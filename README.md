# STATION 9

A Minecraft horror map, about **25–30 minutes**. Java Edition **1.20.4**, vanilla, singleplayer.

## Install

1. Unzip `Station 9.zip` into your saves folder (macOS: `~/Library/Application Support/minecraft/saves/`).
2. Open the world **Station 9** in Minecraft **1.20.4** (Lunar Client is fine).
3. The map starts by itself. The world's sounds and textures load automatically (they're `resources.zip` inside the world).

**Turn your sound up and your brightness down. Headphones help.**

## How to play

| | |
|---|---|
| **Flashlight** | Hold it and **right-click** to switch it on or off. It drains its battery. Spare batteries swap in automatically; look for them. |
| **Sneak** | Walking makes a little noise, sprinting carries a long way, sneaking is silent. |
| **Lockers** | Step into a metal locker and **close the door** behind you to hide. |
| **Objectives** | Shown top-right. Reyes will talk you through it on the radio. |
| **Restart** | `/function station9:start`, or click the link in chat when you rejoin. |

The rules of the thing down there are in the logs and on the tapes. Read them.
There are **two endings**.

## Files

| Path | What it is |
|---|---|
| `Station 9/`, `Station 9.zip` | The ready-to-play world (datapack and resource pack installed) |
| `Station9/` | The datapack on its own (generated) |
| `generate.py` + `s9/` | Build the datapack and the resource pack. Every room, light, scare and line is defined here |
| `tools/make_audio.py` | Makes every sound: the voice acting (text-to-speech) and the effects |
| `assets/sounds/` | The generated sounds |
| `tests/` | A test server, a bot player and scripted playthroughs |
| `BRIEF.md` | Technical handoff notes |

## Tuning

- `s9/ai.py` `SPEED`: how fast Subject 9 wanders, hunts, lunges and chases.
- `s9/systems.py` `BATTERY_TICKS`: how long a battery lasts (3 minutes).
- `s9/story.py` `HEADSTART`: how long you get between the blackout and the breach.

Rebuild with `python3 generate.py`, then `python3 tests/make_world.py` to make a fresh world.
