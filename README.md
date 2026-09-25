# STATION 9

A short Minecraft horror map (about 10 minutes). Java Edition **1.20.4**, vanilla, singleplayer.

## Play
Open the world **Station 9** in Minecraft 1.20.4. The map starts automatically.
Turn your sound up and your brightness down. Headphones help.

- Restart at any point: `/function station9:start` (a clickable link also shows in chat)
- Share it: send someone `Station 9.zip` and have them unzip it into `.minecraft/saves`

## Files
| File | What it is |
|---|---|
| `Station 9/` and `Station 9.zip` | The ready-to-play world |
| `Station9/` and `Station9-datapack.zip` | The datapack by itself. To install it in your own world, use a Superflat "The Void" world with cheats on, then run `/function station9:start` |
| `generate.py` | Builds the datapack. Every room, light, scare and timing is defined here |
| `package_world.py` | Turns a server-built world into a singleplayer save |

## Tuning (top of `generate.py`)
- `HUNTER_SPEED`: how fast Subject 9 chases (0.34). Raise it for a harder chase, lower it for an easier one.
- `HUNTER_LEASH`: how far behind it can fall before it catches back up (16 blocks).
- `HUNTER_HEADSTART` / `RESPAWN_GRACE`: how many ticks of head start you get.

Rebuild with `python3 generate.py`, copy `Station9/` into the world's `datapacks/` folder, then run `/reload` and `/function station9:start` in game.
