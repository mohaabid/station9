#!/usr/bin/env python3
"""
Make every sound in STATION 9: the voice acting and the sound effects.

    pip install numpy scipy soundfile piper-tts
    python3 tools/make_audio.py              # everything
    python3 tools/make_audio.py voices       # just the dialogue
    python3 tools/make_audio.py sfx          # just the effects and ambience

Voices are read by Piper (offline neural text-to-speech). The .onnx voice models are
downloaded to ~/.station9-voices on first use. Effects are synthesised from scratch.
Output: assets/sounds/**.ogg plus assets/sounds/manifest.json (durations, used by
generate.py to time scenes).

Mono files are positional in game (footsteps, doors). Stereo files play at the same
volume wherever you walk, which is what voices, ambience and stingers need.
"""
import json
import os
import sys
import urllib.request

import numpy as np
import soundfile as sf
from scipy import linalg, signal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from s9.script import L, SPEAKERS  # noqa: E402

OUT = os.path.join(ROOT, "assets", "sounds")
VOICES = os.path.expanduser("~/.station9-voices")
SR = 44100
rng = np.random.default_rng(9)
manifest = {}


# =========================================================================
# DSP helpers
# =========================================================================
def secs(n):
    return int(round(n * SR))


def silence(t):
    return np.zeros(secs(t))


def tvec(t):
    return np.arange(secs(t)) / SR


def white(t):
    return rng.standard_normal(secs(t))


def pink(t):
    n = secs(t)
    spec = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    f[0] = f[1]
    x = np.fft.irfft(spec / np.sqrt(f), n)
    return x / (np.std(x) + 1e-12)


def brown(t):
    x = np.cumsum(rng.standard_normal(secs(t)))
    x = filt(x, "high", 15, 2)
    return x / (np.std(x) + 1e-12)


def filt(x, kind, f, order=4):
    sos = signal.butter(order, f, btype=kind, fs=SR, output="sos")
    return signal.sosfilt(sos, x, axis=0)


def band(x, lo, hi, order=4):
    return filt(x, "band", [lo, hi], order)


def reson(x, f, q):
    """Resonant peak (a single formant)."""
    b, a = signal.iirpeak(f, q, fs=SR)
    return signal.lfilter(b, a, x)


def env_exp(t, tau, attack=0.002):
    tt = tvec(t)
    e = np.exp(-tt / tau)
    na = max(1, secs(attack))
    e[:na] *= np.linspace(0, 1, na)
    return e


def env_ar(t, attack, release):
    n = secs(t)
    e = np.ones(n)
    na, nr = min(n, secs(attack)), min(n, secs(release))
    if na:
        e[:na] = np.linspace(0, 1, na) ** 2
    if nr:
        e[n - nr:] *= np.linspace(1, 0, nr) ** 2
    return e


def fade(x, fin=0.01, fout=0.05):
    x = x.copy()
    ni, no = min(len(x), secs(fin)), min(len(x), secs(fout))
    if ni:
        x[:ni] *= np.linspace(0, 1, ni)[:, None] if x.ndim == 2 else np.linspace(0, 1, ni)
    if no:
        x[len(x) - no:] *= np.linspace(1, 0, no)[:, None] if x.ndim == 2 else np.linspace(1, 0, no)
    return x


def mix(length, *parts):
    """parts: (signal, start_seconds, gain)."""
    out = np.zeros(secs(length))
    for x, start, gain in parts:
        i = secs(start)
        if i >= len(out):
            continue
        n = min(len(x), len(out) - i)
        out[i:i + n] += x[:n] * gain
    return out


def sweep(f0, f1, t, curve="exp"):
    """Phase of a sine gliding from f0 to f1."""
    n = secs(t)
    f = np.geomspace(f0, f1, n) if curve == "exp" else np.linspace(f0, f1, n)
    return 2 * np.pi * np.cumsum(f) / SR


def saw(phase):
    return 2 * ((phase / (2 * np.pi)) % 1.0) - 1


def modal(freqs, decays, amps, t):
    tt = tvec(t)
    out = np.zeros_like(tt)
    for f, d, a in zip(freqs, decays, amps):
        out += a * np.sin(2 * np.pi * f * tt + rng.uniform(0, 6.28)) * np.exp(-tt / d)
    return out


def pluck(f, t, decay=0.996):
    n = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, n)
    out = np.zeros(secs(t))
    for i in range(len(out)):
        j = i % n
        out[i] = buf[j]
        buf[j] = decay * 0.5 * (buf[j] + buf[(j + 1) % n])
    return out


def reverb(x, t60=1.4, wet=0.3, lp=5000, stereo=False, pre=0.012):
    n = secs(t60 * 1.2)
    tt = np.arange(n) / SR

    def ir():
        r = rng.standard_normal(n) * np.exp(-6.9 * tt / t60)
        r = filt(r, "low", lp, 2)
        r[:secs(pre)] = 0
        return r / np.sqrt(np.sum(r ** 2))

    dry = np.concatenate([x, np.zeros(n)])

    def wet_part():
        w = signal.fftconvolve(x, ir())[:len(dry)]
        return np.pad(w, (0, len(dry) - len(w)))

    if stereo:
        wl, wr = wet_part(), wet_part()
        return np.stack([dry * (1 - wet) + wl * wet, dry * (1 - wet) + wr * wet], axis=1)
    return dry * (1 - wet) + wet_part() * wet


def drive(x, amount):
    return np.tanh(x * amount) / np.tanh(amount)


def resample(x, ratio):
    """Play back `ratio` times faster (pitch and speed together)."""
    from fractions import Fraction
    fr = Fraction(ratio).limit_denominator(200)
    return signal.resample_poly(x, fr.denominator, fr.numerator, axis=0)


def compress(x, thresh=0.3, ratio=4.0, win=0.01):
    envl = np.sqrt(signal.convolve(x ** 2, np.ones(secs(win)) / secs(win), mode="same")) + 1e-9
    gain = np.where(envl > thresh, (thresh + (envl - thresh) / ratio) / envl, 1.0)
    return x * gain


def norm(x, peak_db=-1.0):
    p = np.max(np.abs(x)) + 1e-12
    return x * (10 ** (peak_db / 20) / p)


def stereo(x, width=0.0):
    if x.ndim == 2:
        return x
    if width <= 0:
        return np.stack([x, x], axis=1)
    d = secs(0.011)
    other = np.concatenate([np.zeros(d), x[:-d]])
    return np.stack([x, x * (1 - width) + other * width], axis=1)


def save(name, x, kind="sfx", peak_db=-1.0, is_stereo=None):
    x = np.asarray(x, dtype=np.float64)
    if not np.all(np.isfinite(x)):
        raise ValueError(f"{name}: non-finite samples")
    x = x - np.mean(x, axis=0)
    x = fade(norm(x, peak_db), 0.003, 0.02)
    if is_stereo:
        x = stereo(x)
    path = os.path.join(OUT, f"{name}.ogg")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = x.astype(np.float32)
    with sf.SoundFile(path, "w", SR, 2 if data.ndim == 2 else 1, format="OGG", subtype="VORBIS") as f:
        for i in range(0, len(data), 8192):      # one big write crashes libsndfile's vorbis encoder
            f.write(data[i:i + 8192])
    manifest[name] = dict(dur=round(len(x) / SR, 3), stereo=bool(x.ndim == 2), kind=kind)
    print(f"  {name:28s} {len(x) / SR:6.2f}s {'stereo' if x.ndim == 2 else 'mono'}")


# =========================================================================
# VOICES
# =========================================================================
_voice_cache = {}


def voice_model(model):
    if model in _voice_cache:
        return _voice_cache[model]
    from piper import PiperVoice
    os.makedirs(VOICES, exist_ok=True)
    onnx = os.path.join(VOICES, model + ".onnx")
    lang, rest = model.split("-", 1)
    name, quality = rest.rsplit("-", 1)
    base = f"https://huggingface.co/rhasspy/piper-voices/resolve/main/{lang.split('_')[0]}/{lang}/{name}/{quality}/{model}"
    for ext in (".onnx", ".onnx.json"):
        if not os.path.exists(onnx.replace(".onnx", ext)):
            print(f"  downloading {model}{ext}")
            urllib.request.urlretrieve(base + ext, onnx.replace(".onnx", ext))
    _voice_cache[model] = PiperVoice.load(onnx)
    return _voice_cache[model]


def tts(model, text, speed=1.0, noise=0.6):
    from piper.config import SynthesisConfig
    v = voice_model(model)
    cfg = SynthesisConfig(length_scale=speed, noise_scale=noise, noise_w_scale=0.8)
    chunks = list(v.synthesize(text, syn_config=cfg))
    x = np.concatenate([c.audio_float_array for c in chunks]).astype(np.float64)
    sr = chunks[0].sample_rate
    x = signal.resample_poly(x, SR, sr)
    # trim the model's leading/trailing silence
    idx = np.where(np.abs(x) > 0.01)[0]
    if len(idx):
        x = x[max(0, idx[0] - secs(0.03)):idx[-1] + secs(0.08)]
    return x


def lpc(frame, order):
    spec = np.fft.rfft(frame, 2 * len(frame))
    r = np.fft.irfft(np.abs(spec) ** 2)[:order + 1]
    if r[0] <= 1e-9:
        return None
    r[0] *= 1.0001
    a = linalg.solve_toeplitz(r[:order], r[1:order + 1])
    return np.concatenate([[1.0], -a])


def whisperize(x, order=20):
    """Swap the voice's buzz for breath, keeping the mouth shapes: real whispered words."""
    n = secs(0.03)
    hop = n // 4
    win = np.hanning(n)
    out = np.zeros(len(x) + n)
    for i in range(0, len(x) - n, hop):
        seg = x[i:i + n] * win
        a = lpc(seg, order)
        if a is None or not np.all(np.isfinite(a)):
            continue
        g = np.sqrt(np.mean(signal.lfilter(a, [1.0], seg) ** 2))
        y = signal.lfilter([1.0], a, rng.standard_normal(n) * g)
        if np.all(np.isfinite(y)) and np.max(np.abs(y)) < 50:
            out[i:i + n] += y * win
    return band(out, 250, 9000)


def squelch(t, level=1.0):
    s = band(white(t), 800, 6000) * env_exp(t, t / 3)
    return s * level


def radio_fx(v):
    v = band(v, 320, 3300, 6)
    v = drive(norm(v, -3) * 1.0, 2.2)
    v = compress(v, 0.25, 3)
    n = len(v) / SR
    bed = band(pink(n + 0.6), 500, 5000) * 0.035
    body = mix(n + 0.6, (v, 0.2, 0.85), (bed, 0, 1.0), (squelch(0.16), 0, 0.5), (squelch(0.22), n + 0.3, 0.35))
    return stereo(body)


def garble_fx(v):
    n = len(v) / SR
    gate = np.ones(len(v))
    t = 0.0
    while t < n:
        seg = rng.uniform(0.12, 0.45)
        if rng.random() < 0.45:
            a, b = secs(t), secs(t + seg)
            gate[a:b] = 0.0
        t += seg
    gate = signal.convolve(gate, np.ones(secs(0.01)) / secs(0.01), mode="same")
    v = band(v, 400, 2800, 6) * gate
    v = drive(norm(v, -3), 3.5)
    crackle = band(white(n), 1000, 7000) * (1 - gate) * 0.5
    stat = band(pink(n), 600, 6000) * 0.12
    out = v * 0.8 + crackle + stat
    out = mix(n + 0.5, (out, 0.15, 1.0), (squelch(0.2), 0, 0.6), (squelch(0.3), n + 0.2, 0.5))
    return stereo(out)


def chime():
    t = 1.3
    a = modal([659.3, 1318.6, 1977.8], [0.5, 0.3, 0.2], [1, 0.3, 0.1], t)
    b = modal([523.3, 1046.5, 1569.8], [0.6, 0.35, 0.2], [1, 0.3, 0.1], t)
    return mix(1.6, (a, 0, 0.5), (b, 0.45, 0.5))


def pa_fx(v):
    v = band(v, 220, 6000, 4)
    v = compress(norm(v, -3), 0.3, 3)
    c = chime()
    n = len(v) / SR + 1.7
    dry = mix(n, (c, 0, 0.7), (v, 1.4, 1.0))
    return reverb(dry, t60=2.2, wet=0.4, lp=4000, stereo=True)


def wow(v, depth=0.0025, rate=0.55, flutter=0.0006, frate=7.0):
    n = len(v)
    tt = np.arange(n) / SR
    speed = 1 + depth * np.sin(2 * np.pi * rate * tt) + flutter * np.sin(2 * np.pi * frate * tt)
    pos = np.cumsum(speed)
    pos = pos[pos < n - 1]
    return np.interp(pos, np.arange(n), v)


def clunk():
    return filt(white(0.08), "low", 900) * env_exp(0.08, 0.015) + modal([180, 410], [0.05, 0.03], [0.6, 0.2], 0.08)


def tape_fx(v, shaky=False):
    v = wow(v, depth=0.004 if shaky else 0.0025)
    if shaky:
        tt = np.arange(len(v)) / SR
        v = v * (1 - 0.12 * (0.5 + 0.5 * np.sin(2 * np.pi * 5.3 * tt)))
    v = band(v, 160, 5200, 4)
    v = drive(norm(v, -3), 1.6)
    n = len(v) / SR + 1.2
    hiss = filt(pink(n), "high", 2500) * 0.03 + filt(brown(n), "low", 120) * 0.02
    out = mix(n, (clunk(), 0, 0.8), (hiss, 0, 1.0), (v, 0.45, 0.9), (clunk(), n - 0.35, 0.7))
    return stereo(out)


def phone_fx(v):
    v = resample(v, 0.91)                     # a little slow and a little low: almost her
    v = band(v, 420, 3000, 6)
    v = drive(norm(v, -3), 2.8)
    n = len(v) / SR
    line = band(pink(n + 2.5), 300, 3400) * 0.03 + np.sin(2 * np.pi * 50 * tvec(n + 2.5)) * 0.01
    tail = band(white(1.4), 300, 3000) * env_ar(1.4, 0.4, 0.8) * 0.15
    out = mix(n + 2.5, (line, 0, 1.0), (v, 0.3, 0.9), (tail, n + 0.8, 1.0))
    return stereo(out)


def whisper_fx(v):
    w = whisperize(v)
    w = reverb(w, t60=0.6, wet=0.2, lp=7000)
    return stereo(norm(w, -3), width=0.6)


def make_voices():
    print("voices:")
    for key, ln in L.items():
        label, color, model, style = SPEAKERS[ln["who"]]
        v = tts(model, ln["say"], ln["speed"], noise=0.7 if style == "tape_shaky" else 0.6)
        if style == "radio":
            out = radio_fx(v)
        elif style == "garble":
            out = garble_fx(v)
        elif style == "pa":
            out = pa_fx(v)
        elif style == "tape":
            out = tape_fx(v)
        elif style == "tape_shaky":
            out = tape_fx(v, shaky=True)
        elif style == "phone":
            out = phone_fx(v)
        elif style == "whisper":
            out = whisper_fx(v)
        else:
            raise ValueError(style)
        save(f"voice/{key}", out, "voice", peak_db=-2.0)


# =========================================================================
# EFFECTS
# =========================================================================
def creature_step(i):
    t = 0.55
    thump = np.sin(sweep(85 + 10 * i, 38, 0.2)) * env_exp(0.2, 0.06)
    body = filt(white(t), "low", 380 + 60 * i) * env_exp(t, 0.05)
    grit = band(white(t), 1800, 5000) * env_exp(t, 0.02) * 0.25
    claw = band(white(0.12), 2500 + 300 * i, 6000) * env_exp(0.12, 0.03) * 0.35
    drag = band(white(0.3), 600, 2400) * env_ar(0.3, 0.08, 0.2) * 0.1
    out = mix(t, (thump, 0, 1.0), (body, 0, 0.6), (grit, 0.005, 1.0), (claw, 0.04 + 0.02 * i, 1.0), (drag, 0.12, 1.0))
    return reverb(out, 0.5, 0.15, 3000)


def creature_breath(i):
    t = 2.2 + 0.3 * i
    n = pink(t)
    e = env_ar(t, 0.5, 1.0) * (1 + 0.25 * np.sin(2 * np.pi * (0.9 + 0.2 * i) * tvec(t)))
    fry = np.clip(saw(2 * np.pi * np.cumsum(np.full(secs(t), 31.0 + 4 * i)) / SR), -0.2, 1.0)
    fry = filt(fry, "low", 400) * 0.6
    src = n * (0.6 + 0.4 * np.abs(fry))
    v = reson(src, 320 - 20 * i, 3) + reson(src, 860, 4) * 0.6 + reson(src, 2300, 6) * 0.25
    v = band(v, 90, 4000) * e
    return reverb(v, 0.8, 0.2, 2500)


def sniff(i):
    t = 1.3
    parts = []
    at = 0.0
    for k in range(3 + i):
        d = rng.uniform(0.07, 0.12)
        s = band(white(d), 1200, 5500) * env_ar(d, 0.02, 0.05)
        parts.append((s, at, rng.uniform(0.7, 1.0)))
        at += d + rng.uniform(0.05, 0.1)
    long_ = band(white(0.4), 900, 4500) * env_ar(0.4, 0.1, 0.25)
    parts.append((long_, at + 0.1, 0.9))
    return reverb(mix(t, *parts), 0.5, 0.2, 4000)


def scream():
    t = 2.2
    out = np.zeros(secs(t))
    for k, (f0, f1) in enumerate([(420, 1350), (560, 1800), (300, 900), (700, 2100)]):
        vib = 1 + 0.03 * np.sin(2 * np.pi * (6 + k) * tvec(t))
        ph = sweep(f0, f1, t) * vib
        s = saw(ph) * 0.6 + np.sin(ph * 1.5) * 0.3
        out += s * env_ar(t, 0.05, 0.9) * (0.7 if k else 1.0)
    out = reson(out, 1100, 2) + reson(out, 2600, 3) * 0.7 + out * 0.2
    growl = drive(filt(saw(sweep(70, 50, t)), "low", 600) * env_ar(t, 0.02, 1.0), 3) * 0.8
    noise_ = band(white(t), 2000, 9000) * env_ar(t, 0.01, 1.2) * 0.6
    out = drive(norm(out + growl + noise_, -3), 2.5)
    return reverb(out, 1.6, 0.35, 6000, stereo=True)


def sting(kind):
    if kind == "hit":
        t = 5.0
        notes = [65.4, 69.3, 185.0, 196.0, 392.0, 415.3, 1244.5]
        out = np.zeros(secs(t))
        for k, f in enumerate(notes):
            det = [0.997, 1.0, 1.004]
            s = sum(saw(2 * np.pi * f * d * tvec(t)) for d in det) / 3
            out += filt(s, "low", 900 + 300 * k) * env_exp(t, 0.9 + 0.2 * k, 0.004)
        boom = np.sin(sweep(60, 30, 1.5)) * env_exp(1.5, 0.4)
        out = mix(t, (out, 0, 0.5), (boom, 0, 0.9), (band(white(0.4), 2000, 8000) * env_exp(0.4, 0.08), 0, 0.3))
        return reverb(out, 2.8, 0.45, 4000, stereo=True)
    # dread: a slow cluster swelling up out of nothing
    t = 6.0
    notes = [55.0, 58.3, 82.4, 87.3, 164.8, 174.6, 233.1]
    out = np.zeros(secs(t))
    for k, f in enumerate(notes):
        s = sum(saw(2 * np.pi * f * d * tvec(t) + k) for d in (0.996, 1.0, 1.005)) / 3
        out += filt(s, "low", 500 + 150 * k)
    e = (np.linspace(0, 1, secs(t)) ** 2.5)
    e[-secs(0.6):] *= np.linspace(1, 0, secs(0.6))
    out = out * e + band(pink(t), 200, 2000) * e * 0.2
    return reverb(out, 3.0, 0.4, 3000, stereo=True)


def roof_step(i):
    t = 1.2
    hit = modal([143 + 9 * i, 257, 389 + 13 * i, 611, 877 + 21 * i, 1290], [0.5, 0.4, 0.35, 0.25, 0.2, 0.12],
                [0.8, 0.6, 0.5, 0.35, 0.25, 0.15], t)
    thud = np.sin(sweep(70, 35, 0.3)) * env_exp(0.3, 0.08)
    click = band(white(0.03), 1500, 6000) * env_exp(0.03, 0.006)
    return reverb(mix(t, (hit * env_exp(t, 0.35), 0, 0.6), (thud, 0, 1.0), (click, 0, 0.4)), 0.9, 0.25, 3000)


def roof_thump():
    t = 2.5
    hit = modal([97, 151, 233, 377, 522, 811, 1170], [1.2, 1.0, 0.8, 0.6, 0.5, 0.35, 0.25], [1, 0.8, 0.7, 0.5, 0.4, 0.3, 0.2], t)
    boom = np.sin(sweep(55, 28, 0.8)) * env_exp(0.8, 0.25)
    rattle = band(white(0.8), 1500, 5000) * env_exp(0.8, 0.2) * (np.abs(np.sin(2 * np.pi * 23 * tvec(0.8))))
    return reverb(mix(t, (hit, 0, 0.7), (boom, 0, 1.0), (rattle, 0.02, 0.3)), 1.3, 0.3, 3000)


def scrape():
    t = 3.6
    out = np.zeros(secs(t))
    pos = 0.05
    while pos < t - 0.4:
        imp = np.zeros(secs(0.05))
        imp[0] = rng.uniform(0.3, 1.0)
        out[secs(pos):secs(pos) + len(imp)] += imp
        pos += rng.uniform(0.004, 0.014)
    metal = sum(reson(out, f, 40) * a for f, a in [(611, 0.5), (1290, 0.4), (1877, 0.3), (2710, 0.2)])
    squeal = np.sin(sweep(1900, 1400, t) + 0.3 * np.sin(2 * np.pi * 7 * tvec(t))) * env_ar(t, 0.8, 1.2) * 0.12
    e = env_ar(t, 0.2, 0.8)
    return reverb((metal + squeal) * e, 1.2, 0.3, 4000)


def crash():
    t = 7.0
    snap = band(white(0.05), 500, 9000) * env_exp(0.05, 0.01)
    twang = pluck(92, 2.2, 0.9985) * env_exp(2.2, 0.8)
    fall = band(pink(1.3), 60, 900) * np.linspace(0.2, 1, secs(1.3))
    impact = modal([61, 97, 151, 233, 377, 610, 987], [1.5, 1.2, 1.0, 0.8, 0.6, 0.4, 0.3], [1, 1, 0.8, 0.6, 0.5, 0.4, 0.3], 4)
    boom = np.sin(sweep(48, 22, 2)) * env_exp(2, 0.6)
    debris = band(white(3), 300, 6000) * env_exp(3, 0.5)
    taps = []
    at = 2.2
    for k in range(9):
        at += rng.uniform(0.12, 0.6)
        d = modal([rng.uniform(600, 2400)], [0.08], [1], 0.2)
        taps.append((d, at, 0.3 * rng.uniform(0.3, 1)))
    out = mix(t, (snap, 0, 1.0), (twang, 0.02, 0.5), (fall, 0.3, 0.6), (impact, 1.6, 0.9), (boom, 1.6, 1.0),
              (debris, 1.62, 0.5), *taps)
    return reverb(drive(norm(out, -2), 1.5), 2.0, 0.3, 3500, stereo=True)


def lift_ride():
    t = 64.0
    tt = tvec(t)
    f = 48 + 1.5 * np.sin(2 * np.pi * 0.05 * tt)
    ph = 2 * np.pi * np.cumsum(f) / SR
    motor = filt(saw(ph) + 0.5 * saw(2 * ph), "low", 260) * 0.35
    whine = np.sin(2 * np.pi * np.cumsum(420 + 6 * np.sin(2 * np.pi * 0.11 * tt)) / SR) * 0.03
    rumble = filt(brown(t), "low", 140) * 0.5
    wind = band(pink(t), 200, 1400) * (0.1 + 0.05 * np.sin(2 * np.pi * 0.07 * tt))
    parts = [(motor + whine + rumble + wind, 0, 1.0)]
    at = 3.0
    while at < t - 3:
        at += rng.uniform(4.5, 11.0)
        c = modal([rng.uniform(300, 900), rng.uniform(900, 2000)], [0.25, 0.12], [1, 0.4], 0.5) * 0.25
        parts.append((c, at, rng.uniform(0.3, 0.7)))
    out = mix(t, *parts) * env_ar(t, 2.0, 2.0)
    return stereo(out, width=0.5)


def wind_ambience():
    t = 60.0
    tt = tvec(t)
    gust = 0.5 + 0.5 * np.sin(2 * np.pi * 0.045 * tt) * np.sin(2 * np.pi * 0.013 * tt + 1)
    w = pink(t)
    low = filt(w, "low", 500) * (0.4 + 0.6 * gust)
    hi = band(pink(t), 700, 2500) * (0.05 + 0.25 * gust ** 2)
    parts = [(low + hi, 0, 1.0)]
    for at in (14.0, 41.0):
        g = modal([97, 140, 211], [1.4, 1.1, 0.8], [1, 0.6, 0.4], 3) * env_ar(3, 0.8, 1.5) * 0.3
        parts.append((g, at, 1.0))
    out = mix(t, *parts)
    l, r = out, np.roll(out, secs(0.2))
    x = np.stack([l, r], axis=1)
    return loopable(x)


def loopable(x, xf=2.0):
    """Crossfade the tail into the head so back-to-back plays don't seam."""
    n = secs(xf)
    head, tail = x[:n], x[-n:]
    ramp = np.linspace(0, 1, n)[:, None] if x.ndim == 2 else np.linspace(0, 1, n)
    x = x[:-n].copy()
    x[:n] = head * ramp + tail * (1 - ramp)
    return x


def room_ambience(deep):
    t = 60.0
    tt = tvec(t)
    base = filt(brown(t), "low", 160 if deep else 220) * 0.6
    hum_f = 38.0 if deep else 50.0
    hum = (np.sin(2 * np.pi * hum_f * tt) + 0.5 * np.sin(2 * np.pi * hum_f * 1.5 * tt + 0.3 * np.sin(2 * np.pi * 0.03 * tt))) * 0.12
    air = band(pink(t), 300, 1800) * (0.05 + 0.03 * np.sin(2 * np.pi * 0.021 * tt))
    parts = [(base + hum + air, 0, 1.0)]
    events = [7.0, 19.5, 33.0, 47.0] if deep else [11.0, 36.0]
    for at in events:
        if deep:
            g = np.sin(sweep(rng.uniform(70, 110), rng.uniform(40, 60), 4)) * env_ar(4, 1.5, 2) * 0.25
            g += reson(band(pink(4), 80, 1000), rng.uniform(150, 300), 20) * env_ar(4, 1.0, 2.0) * 0.1
        else:
            g = modal([rng.uniform(80, 160), rng.uniform(200, 400)], [0.6, 0.3], [1, 0.5], 1.5) * 0.25
        parts.append((g, at + rng.uniform(-2, 2), 1.0))
    out = mix(t, *parts)
    return loopable(stereo(reverb(out, 1.8, 0.25, 1500)[:secs(t)], width=0.8))


def siren():
    t = 9.5
    n = secs(t)
    tt = tvec(t)
    f = np.interp(tt, [0, 3.2, 4.8, 9.5], [180, 640, 640, 150])
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = saw(ph) * 0.5 + np.sign(np.sin(ph)) * 0.2 + np.sin(2 * ph) * 0.2
    s = filt(s, "low", 2200) * env_ar(t, 0.4, 2.0)
    s += band(pink(t), 400, 3000) * 0.04 * env_ar(t, 0.4, 2.0)
    return reverb(s[:n], 2.5, 0.45, 3000, stereo=True)


def static_burst(i):
    t = 0.35 + 0.15 * i
    s = band(white(t), 700, 6500) * (0.4 + 0.6 * (rng.random(secs(t)) > 0.6))
    return stereo(s * env_ar(t, 0.01, 0.1))


def phone_ring():
    def ring(d):
        partials = modal([1130, 1130 * 2.76, 1130 * 5.4], [0.05, 0.03, 0.02], [1, 0.4, 0.2], 0.06)
        out = np.zeros(secs(d))
        at = 0
        while at < secs(d) - len(partials):
            out[at:at + len(partials)] += partials * rng.uniform(0.8, 1.0)
            at += secs(1 / 21)
        return out
    t = 7.5
    return reverb(mix(t, (ring(1.9), 0.05, 1.0), (ring(1.9), 3.9, 1.0)), 0.7, 0.25, 6000)


def handset(up=True):
    t = 0.9
    c = modal([220, 530, 1250], [0.06, 0.04, 0.02], [1, 0.5, 0.3], 0.2)
    line = band(white(0.7), 300, 3400) * 0.1 * (env_ar(0.7, 0.05, 0.3) if up else 0)
    return stereo(mix(t, (c, 0, 0.9), (line, 0.1, 1.0)))


def locker(opening):
    t = 0.9
    latch = modal([900, 2100, 3300], [0.04, 0.02, 0.015], [1, 0.5, 0.3], 0.1)
    creak_f = np.interp(tvec(0.5), [0, 0.5], [620, 480] if opening else [480, 700])
    creak = np.sin(2 * np.pi * np.cumsum(creak_f * (1 + 0.04 * rng.standard_normal(secs(0.5)))) / SR)
    creak = band(creak, 300, 3000) * env_ar(0.5, 0.1, 0.2) * 0.25
    body = modal([210, 330, 520], [0.2, 0.15, 0.1], [1, 0.6, 0.4], 0.4)
    if opening:
        out = mix(t, (latch, 0, 0.6), (creak, 0.06, 1.0), (body, 0.05, 0.2))
    else:
        out = mix(t, (creak, 0, 0.6), (body, 0.35, 0.8), (latch, 0.36, 0.7))
    return reverb(out, 0.4, 0.15, 5000)


def flash_click(on):
    t = 0.12
    c = band(white(0.012), 2000, 8000) * env_exp(0.012, 0.002)
    c2 = modal([3200 if on else 2600], [0.01], [1], 0.03)
    return stereo(mix(t, (c, 0, 0.7), (c2, 0.004, 0.5)))


def flash_buzz():
    t = 0.7
    out = np.zeros(secs(t))
    at = 0.0
    while at < t - 0.05:
        d = rng.uniform(0.01, 0.06)
        b = saw(2 * np.pi * 120 * tvec(d)) * 0.4 + band(white(d), 2000, 8000) * 0.5
        out[secs(at):secs(at) + len(b)] += b[:len(out) - secs(at)]
        at += d + rng.uniform(0.01, 0.12)
    return stereo(band(out, 100, 9000))


def gen_start():
    t = 8.0
    tt = tvec(t)
    f = np.interp(tt, [0, 0.4, 5.0, 8.0], [4, 6, 50, 50])
    ph = 2 * np.pi * np.cumsum(f) / SR
    motor = filt(saw(ph) + 0.6 * saw(2 * ph) + 0.3 * saw(3 * ph), "low", 700) * 0.4
    whine = np.sin(2 * np.pi * np.cumsum(f * 18) / SR) * 0.06
    clk = mix(0.6, (modal([140, 320, 900], [0.3, 0.2, 0.08], [1, 0.6, 0.3], 0.5), 0, 1.0))
    out = mix(t, (motor * env_ar(t, 0.3, 0.5), 0, 1.0), (whine * env_ar(t, 2, 0.5), 0, 1.0), (clk, 0, 0.9))
    return reverb(out, 1.5, 0.25, 3000, stereo=True)


def lights_on():
    t = 3.5
    parts = []
    for k, at in enumerate([0.0, 0.42, 0.95]):
        c = modal([120 + 20 * k, 290, 700, 1500], [0.35, 0.25, 0.12, 0.06], [1, 0.7, 0.4, 0.2], 0.6)
        thud = np.sin(sweep(80, 40, 0.3)) * env_exp(0.3, 0.1)
        parts += [(c, at, 0.7), (thud, at, 0.8)]
    hum = (np.sin(2 * np.pi * 50 * tvec(2.4)) + 0.4 * np.sin(2 * np.pi * 100 * tvec(2.4))) * env_ar(2.4, 0.8, 1.2) * 0.3
    parts.append((hum, 1.0, 1.0))
    return reverb(mix(t, *parts), 1.8, 0.3, 3000, stereo=True)


def bang(i):
    t = 2.2
    door = modal([88 + 7 * i, 143, 236, 371, 590, 930], [0.9, 0.7, 0.5, 0.4, 0.3, 0.2], [1, 0.8, 0.6, 0.4, 0.3, 0.2], t)
    boom = np.sin(sweep(60, 30, 0.6)) * env_exp(0.6, 0.18)
    crack = band(white(0.04), 400, 7000) * env_exp(0.04, 0.008)
    rattle = band(white(0.6), 1000, 5000) * env_exp(0.6, 0.15) * np.abs(np.sin(2 * np.pi * 31 * tvec(0.6)))
    out = mix(t, (door, 0, 0.6), (boom, 0, 1.0), (crack, 0, 0.5), (rattle, 0.02, 0.3))
    return reverb(drive(norm(out, -2), 1.8), 1.2, 0.25, 3500)


def collapse():
    t = 6.0
    rumble = filt(brown(t), "low", 200) * env_ar(t, 0.3, 2.5)
    pour = band(pink(t), 400, 5000) * env_ar(t, 0.8, 2.0) * 0.4
    parts = [(rumble, 0, 1.0), (pour, 0.4, 1.0)]
    for k in range(14):
        d = modal([rng.uniform(80, 300), rng.uniform(300, 1200)], [0.3, 0.1], [1, 0.4], 0.5)
        d = mix(0.5, (d, 0, 1.0), (np.sin(sweep(rng.uniform(60, 90), 30, 0.3)) * env_exp(0.3, 0.07), 0, 1.0))
        parts.append((d, rng.uniform(0.1, 4.2), rng.uniform(0.3, 0.9)))
    return reverb(drive(norm(mix(t, *parts), -2), 1.4), 2.0, 0.3, 2500, stereo=True)


def relay_boot():
    t = 2.6
    parts = []
    at = 0.0
    for k in range(7):
        c = modal([rng.uniform(1500, 3500)], [0.012], [1], 0.04)
        parts.append((c, at, rng.uniform(0.4, 0.8)))
        at += rng.uniform(0.06, 0.2)
    chirp = np.sin(sweep(600, 1800, 0.35)) * env_ar(0.35, 0.02, 0.1) * 0.3
    hum = band(pink(1.6), 100, 900) * env_ar(1.6, 0.3, 0.8) * 0.3
    parts += [(chirp, at + 0.1, 1.0), (chirp, at + 0.5, 0.7), (hum, at, 1.0)]
    return mix(t, *parts)


def beep(kind):
    if kind == "key":
        return np.sin(2 * np.pi * 1250 * tvec(0.08)) * env_ar(0.08, 0.003, 0.02)
    if kind == "ok":
        return mix(0.35, (np.sin(2 * np.pi * 1000 * tvec(0.1)) * env_ar(0.1, 0.003, 0.02), 0, 0.8),
                   (np.sin(2 * np.pi * 1500 * tvec(0.16)) * env_ar(0.16, 0.003, 0.05), 0.13, 0.8))
    return saw(2 * np.pi * 180 * tvec(0.45)) * env_ar(0.45, 0.005, 0.05) * 0.6


def heartbeat(i):
    t = 0.7
    lub = np.sin(sweep(62, 40, 0.14)) * env_exp(0.14, 0.04)
    dub = np.sin(sweep(55, 36, 0.12)) * env_exp(0.12, 0.035)
    return stereo(filt(mix(t, (lub, 0, 1.0), (dub, 0.24 + 0.02 * i, 0.7)), "low", 180))


def held_breath(i):
    t = 2.6
    inh = band(pink(0.9), 400, 3500) * env_ar(0.9, 0.3, 0.3)
    exh = band(pink(1.3), 250, 2500) * env_ar(1.3, 0.2, 0.9) * (1 + 0.3 * np.sin(2 * np.pi * 9 * tvec(1.3)))
    return stereo(mix(t, (inh, 0, 0.35), (exh, 1.2 + 0.1 * i, 0.4)), width=0.3)


def door_creak():
    t = 3.2
    f = np.interp(tvec(t), [0, 1, 2.2, 3.2], [180, 320, 260, 380])
    jit = 1 + 0.06 * filt(rng.standard_normal(secs(t)), "low", 30)
    ph = 2 * np.pi * np.cumsum(f * jit) / SR
    s = saw(ph) * (0.5 + 0.5 * (rng.random(secs(t)) > 0.3))
    s = reson(s, 900, 5) + reson(s, 2100, 8) * 0.5
    return reverb(band(s, 150, 5000) * env_ar(t, 0.3, 0.6), 0.9, 0.3, 4000)


def gate(opening):
    t = 2.6
    motor = filt(saw(2 * np.pi * np.cumsum(np.interp(tvec(1.6), [0, 1.6], [30, 45])) / SR), "low", 300) * 0.4
    rattle = band(white(1.6), 800, 4000) * np.abs(np.sin(2 * np.pi * 17 * tvec(1.6))) * 0.25
    slam = modal([95, 160, 270, 440, 720], [0.8, 0.6, 0.4, 0.3, 0.2], [1, 0.8, 0.6, 0.4, 0.3], 1.0)
    out = mix(t, (motor + rattle, 0, 1.0), (slam, 1.5, 0.9 if not opening else 0.5))
    return reverb(out, 1.0, 0.25, 3500)


def knock():
    t = 3.0
    parts = []
    for at in (0.0, 0.31, 0.58, 1.9, 2.35):
        k = modal([118, 197, 331, 529], [0.35, 0.25, 0.18, 0.1], [1, 0.7, 0.5, 0.3], 0.5)
        k = mix(0.5, (k, 0, 1.0), (np.sin(sweep(70, 40, 0.2)) * env_exp(0.2, 0.05), 0, 1.0))
        parts.append((k, at + rng.uniform(-0.03, 0.03), rng.uniform(0.7, 1.0)))
    return reverb(mix(t, *parts), 0.8, 0.2, 3000)


def gen_hum():
    t = 20.0
    tt = tvec(t)
    ph = 2 * np.pi * 50 * tt
    h = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)) * 0.3
    h += band(pink(t), 200, 1500) * 0.06
    return loopable(h)


def silent():
    return np.zeros(secs(0.05))


def make_sfx():
    print("effects:")
    for i in range(4):
        save(f"sfx/step_{i + 1}", creature_step(i), "hostile", -2)
    for i in range(3):
        save(f"sfx/breath_{i + 1}", creature_breath(i), "hostile", -3)
    for i in range(2):
        save(f"sfx/sniff_{i + 1}", sniff(i), "hostile", -3)
    save("sfx/scream", scream(), "hostile", -0.5)
    save("sfx/sting_hit", sting("hit"), "master", -1)
    save("sfx/sting_dread", sting("dread"), "master", -3)
    for i in range(3):
        save(f"sfx/roof_step_{i + 1}", roof_step(i), "hostile", -2)
    save("sfx/roof_thump", roof_thump(), "hostile", -1)
    save("sfx/scrape", scrape(), "hostile", -2)
    save("sfx/crash", crash(), "master", -0.5)
    save("amb/lift_ride", lift_ride(), "ambient", -6)
    save("amb/wind", wind_ambience(), "ambient", -6)
    save("amb/b8", room_ambience(False), "ambient", -8)
    save("amb/b9", room_ambience(True), "ambient", -7)
    save("sfx/siren", siren(), "master", -2)
    for i in range(3):
        save(f"sfx/static_{i + 1}", static_burst(i), "master", -6)
    save("sfx/phone_ring", phone_ring(), "block", -2)
    save("sfx/phone_up", handset(True), "master", -4)
    save("sfx/phone_down", handset(False), "master", -4)
    save("sfx/locker_open", locker(True), "block", -3)
    save("sfx/locker_close", locker(False), "block", -3)
    save("sfx/flash_on", flash_click(True), "master", -8)
    save("sfx/flash_off", flash_click(False), "master", -8)
    save("sfx/flash_buzz", flash_buzz(), "master", -8)
    save("sfx/gen_start", gen_start(), "block", -2)
    save("sfx/lights_on", lights_on(), "block", -1)
    for i in range(3):
        save(f"sfx/bang_{i + 1}", bang(i), "hostile", -0.5)
    save("sfx/collapse", collapse(), "block", -0.5)
    save("sfx/relay_boot", relay_boot(), "block", -3)
    save("sfx/beep_key", beep("key"), "block", -8)
    save("sfx/beep_ok", beep("ok"), "block", -6)
    save("sfx/beep_bad", beep("bad"), "block", -6)
    for i in range(2):
        save(f"sfx/heartbeat_{i + 1}", heartbeat(i), "master", -3)
    for i in range(2):
        save(f"sfx/held_breath_{i + 1}", held_breath(i), "master", -10)
    save("sfx/door_creak", door_creak(), "block", -3)
    save("sfx/gate_open", gate(True), "block", -2)
    save("sfx/gate_close", gate(False), "block", -1)
    save("sfx/knock", knock(), "hostile", -1)
    save("sfx/gen_hum", gen_hum(), "block", -6)
    save("sfx/silent", silent(), "master", -60)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    mpath = os.path.join(OUT, "manifest.json")
    if os.path.exists(mpath):
        manifest.update(json.load(open(mpath)))
    if what in ("all", "voices"):
        make_voices()
    if what in ("all", "sfx"):
        make_sfx()
    with open(mpath, "w") as f:
        json.dump(dict(sorted(manifest.items())), f, indent=1)
    print(f"{len(manifest)} sounds -> {OUT}")
