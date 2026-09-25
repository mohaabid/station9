# STATION 9: handoff brief

Read this before changing anything. It covers what the map is, how it's built, how it's
tested, and what nobody has been able to check yet.

## 1. History

- **Version 1** (a previous session): a ~10 minute map on one level. The player's verdict:
  *"good honestly but it could expand it was not that scary, no introduction, boring, could hear
  ticking which pissed me off"*. The ticking was heard **throughout the whole game**.
- **Version 2** (this one): rebuilt around that feedback, following the plan the player approved:
  a walkable introduction, a second level, a flashlight, a creature that roams, lockers, a longer
  escape, two endings, voice acting and custom sounds. Target length 20–30 minutes.

### The ticking

Two things played on a near-constant beat through most of v1:

- **Lit candles.** The game makes lit candles crackle at random, and v1 had ~14 of them along the
  main corridor and in the office. All candles are now unlit.
- **The flickering corridor lamp** played `block.redstone_torch.burnout` every ~1.3 s.

Also removed: the alarm beeps, the steady chase heartbeat, the radio clicks, the sculk sensor and
shrieker, and the lift clanks. The resource pack also mutes the vanilla candle, sculk and burnout
sounds. **Rule: nothing repeats on a fixed short interval.** Ambience is long stereo beds;
creature footsteps use a random stride.

## 2. Player environment

- Minecraft Java **1.20.4** via **Lunar Client**, macOS. Stay on 1.20.4: 1.21 renames datapack
  folders and replaces item NBT with components.
- Singleplayer, cheats on in the delivered world (for the restart link).
- Resource pack format **22**, shipped as the world's `resources.zip`.

## 3. The story

| Stage | Where | What happens |
|---|---|---|
| 1 | Surface | Opening shots of the site in a storm, title card |
| 2 | Surface | Walk from the truck to the security hut; sign in; take the kit (flashlight + battery); call the lift |
| 3 | Lift | Ride down with Reyes briefing; something lands on the cage roof and walks across it; the cable snaps at B8 |
| 4 | B8 | Door release; comms relay restores the radio; find the stairwell code (**0214**: Okafor's note says "the time of the first dip", Hale's tape in the lab says "oh two fourteen", Reyes hints at 4 and 8 min); phone call from "Reyes" who isn't; figure behind the lab glass; the hall changes behind you; lights die on the way down |
| 5 | B9 | First sighting teaches the rule: it creeps closer each time the lamp flickers. Then it roams |
| 6 | B9 | Marsh's keycard in office 9-A (door slams). Mirror scare opens the room behind the mirror: Marsh's body and tape |
| 7 | B9 | Keycard opens containment. It is standing in its cell; the fuse is at its feet |
| 8 | B9 | Fuse taken: blackout, it moves to the generator room and waits |
| 9 | Escape | Lever: every light comes on, lockdown, bangs, blackout, red emergency lights, flashlight burns out, RUN. Tunnel 1, service stairs to B8, service corridor, hall collapses (detour through the cafeteria), lobby, lift. Tunnel 2 is a dead end with a locker |
| 10 | Lift | Ride up. It lands on the roof at ~B4. **Cage light on:** "your cage weight reads wrong", jump scare at the top (**Ending 1, Passenger**). **Cage light off** (Marsh's tape tells you): it can't find you; you walk out into the rain (**Ending 2, Lights Out**) |

Stats at the end: time, deaths, tapes found (of 3), ending.

## 4. How it's built

`python3 generate.py` (stdlib only) writes `Station9/` (datapack, pack_format 26) and
`build/resources.zip` (resource pack). It checks that every called function, sound and predicate
exists and rejects malformed selectors.

| File | Contents |
|---|---|
| `s9/world.py` | **All coordinates**: surface, B8 (floor 50), B9 (floor 40), rooms, openings, doors, lockers, lamps, the creature's waypoint graph and door states |
| `s9/build.py` | Everything that places blocks, split into steps run one per tick on restart |
| `s9/systems.py` | Startup, the tick loop, voices, sidebar objectives, flashlight, batteries, lockers, noise, death, ambience |
| `s9/ai.py` | Subject 9 (below) |
| `s9/story.py` | The acts, scares, chase and endings |
| `s9/script.py` | Every spoken line (shared with the audio tool) |
| `s9/respack.py` | sounds.json, the creature skin, locker doors, item icons (all painted in code) |
| `s9/debug.py` | `debug/b9`, `debug/roam`, `debug/chase`: jump into the story for testing |
| `tools/make_audio.py` | Voices (Piper TTS, offline, models from Hugging Face) + synthesized effects -> `assets/sounds/` with a duration manifest used for timing |

### Subject 9

A NoAI wither skeleton (reskinned) moved by teleport along a waypoint graph. Routes are
precomputed in Python for each door state (`world.TABLES`) and stored as next-hop tables in
command storage. It can't get stuck or lost.

- **Frozen** while the player is looking at it (field of view + line of sight raycast) *and* it's
  lit (light level ≥ 6 at its body, or in the flashlight beam).
- **Sees** the player (hunts) when it has line of sight and the player's flashlight is on or
  they're standing in bright light (≥ 9).
- **Hears** sprinting within 20 blocks, walking within 6. Sneaking is silent.
- **Lockers:** if it saw you within the last 2 s when you closed the door, it walks up and waits
  ~6 s. Opening the door within 4 blocks of it = caught. Otherwise it searches your last spot.
- **Chase:** follows your node at 0.23 blocks/tick (sprint is 0.28), 0.30 when more than 20
  blocks behind, 0.055 while watched and lit.
- **Catch:** camera forced to face it, scream, then death and respawn at the checkpoint with it
  moved far away.

## 5. Lessons (don't repeat these)

1. **Volume selectors** match hitboxes touching `[x, x+dx+1]`. `box_selector()` insets by the
   player half-width. It needs boxes at least 2 wide; use `in_box()` (a predicate) for single cells.
2. **A selector with only `y=`/`dy=`** is a 1-block column at the executor's x/z. The generator
   now rejects partial volume selectors.
3. **Whole-number coordinates are centred** by `tp`/`summon` (48 → 48.5). `fmt()` keeps floats
   as `48.0`.
4. **Changing an existing door with setblock fails**: each half copies the other. `door()` clears
   the door first, then places lower, then upper.
5. Function names must be lowercase. `#minecraft:air` is not a block tag in 1.20.4.
6. `fillbiome` is capped at 32,768 blocks; the surface biome fill is split.
7. Long OGG writes crash libsndfile's Vorbis encoder; `make_audio.py` writes in blocks.
8. Scheduled functions run as the server at world spawn: use `@a` and absolute coordinates.
9. **The test server runs a copy of the datapack.** After `generate.py`, run
   `python3 tests/server.py deploy` or you'll test stale code.
10. Stereo sounds play at full volume wherever the player walks (voices, ambience); mono sounds
    are positional (footsteps, doors).

## 6. How to test

```
python3 tests/server.py setup && python3 tests/server.py start   # 1.20.4 void server + RCON
python3 generate.py && python3 tests/server.py deploy             # after every change
python3 tests/play.py act0 act1 act2 act3                          # the whole map with a bot player
python3 tests/make_world.py                                        # the deliverable world + zip
```

The server jar (sha1 `8dd1a28015f51b1803213892b50b7b4fc76e594d`) lives in `~/.station9-server`.
The bot is mineflayer (`tests/bot/`, `npm install` there). The player accepted the EULA.

**Verified on a real 1.20.4 server:** zero load errors; the full story from first join to both
endings; every voice line in order; the creature's freeze, sight, hearing, hunting, lunge,
locker check, catch and respawn; the chase route including the collapse detour; flashlight
beam and battery swaps; the packaged world auto-starting on first join. Voice lines were checked
for intelligibility with a speech recognizer (Whisper).

**Not verifiable without a person playing:** how scary it is, how hard the chase and the
roaming are, audio balance, the opening camera shots, how the textures look in game, and
whether Lunar Client applies the world resource pack automatically.

## 7. Where to go next

- Ask the player how the chase and the roaming felt, and tune `ai.SPEED` / `HEADSTART`.
- If the resource pack doesn't load in Lunar, the map still works but loses its sounds: check
  first.
- Ideas not built: a secret ending, more rooms on B8, a custom lightmap.
