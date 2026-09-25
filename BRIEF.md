# STATION 9 — Handoff brief for the next Claude

You're picking up a Minecraft horror map that another Claude session built and tested. The player has played it once, and you'll expand it into something actually scary. This file has everything: what exists, how it works, what the player said, the traps we already hit, and how to test and deliver.

**Read this whole file before changing anything.**

---

## 1. The player's verdict (verbatim)

> "good honestly but it could expand it was not that scary, no introduction, boring, could hear ticking which pissed me off"

What that means in practice:

| Complaint | What to do |
|---|---|
| **Not that scary** | The scares are one-shot glimpses, and a figure that stands still and vanishes loses its effect by the second time. The player needs to feel **hunted** well before the finale, and needs **uncertainty**: the same trick shouldn't work the same way twice. |
| **No introduction** | The current intro is about 20 seconds in a dark lift with a title card and a couple of radio lines, under a Blindness effect. It didn't register as an introduction. Build a real opening: who you are, why you're here, what went wrong, and a moment of normality before things turn. |
| **Boring** | About 10 minutes, one objective chain (card → fuse → lever), mostly walking between rooms. There's not enough to do, the spaces are small, and nothing changes as you go. |
| **Ticking that annoyed him** | See section 6. Find the source and remove it. **Ask the player which moment it was** if you can. |

The player agreed to the brief below. Confirm the expansion plan (section 7) with them before you build.

---

## 2. Player environment

- **Minecraft Java 1.20.4** through **Lunar Client** on macOS (Apple Silicon). Stay on 1.20.4. 1.21+ renames datapack folders (`functions/` becomes `function/`) and changes item NBT to components, so this pack would break there.
- Saves folder: `~/Library/Application Support/minecraft/saves/` (the world "Station 9" is installed there).
- Singleplayer, cheats on in the delivered world.
- Vanilla only. No mods. A **resource pack is allowed and encouraged** (1.20.4 resource `pack_format` = **22**). Ship it inside the world as `resources.zip`, which singleplayer loads automatically.

---

## 3. What's in this folder

| Path | What |
|---|---|
| `generate.py` | **The source of truth.** One Python 3 script (stdlib only) that writes the whole datapack: layout, build, lights, scares, chase, ending. Run `python3 generate.py` and it writes `Station9/`. |
| `Station9/` | Generated datapack (1.20.4, `pack_format` 26). Don't edit it by hand; regenerate instead. |
| `package_world.py` | Turns a server-built world into a singleplayer save: renames the level, sets `allowCommands`, adds the icon. It includes a tiny NBT reader/writer. |
| `Station 9.zip` | The current playable world (void world, pre-built, pack installed). |
| `README.md` | Player-facing how-to-play and tuning notes. |
| `BRIEF.md` | This file. |

---

## 4. How the current map works

### Story
You're sent down to Level B9 of an underground research station that went dark 41 days ago. Radio contact is "Ops". The lift crashes on arrival. You need Generator B running.

Lore (from lectern books): Subject 9 is a 2.4 m entity. It only moves in the dark ("it can't SEE in the dark"). Power dips dropped the cell field. Staff member Marsh vanished, and his keycard appeared on Dr. Hale's desk. "The mirrors stopped showing us. Only it." Restoring main power turns every light on at once, and then **it can see you**. That's the twist that triggers the chase.

### Layout (floor y=40, rooms 3 tall at y41–43, ceiling y=44, all carved out of a solid deepslate block)
```
 z
 0   [alcove]            <- fake "reflected office" behind the mirror
 3   [reflection]        <- mirror-image washroom behind the glass
 6   ====mirror====
 7   [washroom]
11   [ OFFICE 9-A  x10-20 ]
18 [LIFT]=[======= CORRIDOR  x7-48 ========]=[ GENERATOR B x50-60, z15-25 ]
     x2-5          [CONTAINMENT x26-36]           |
22                 [   cell x29-33   ]            | tunnel1 x58-59
31                         |tunnel3               |
34                 [======= tunnel2  x35-59 ======]
```
Openings are listed in `OPENINGS`, and lamps in `LAMPS`.

### Flow (`#stage s9`)
| Stage | Meaning | Key triggers |
|---|---|---|
| 0 | Not started | `join` schedules `start` 40 ticks after first join |
| 1 | Lift intro | `intro/0` → `intro/ride` (B1–B8, 30 ticks each) → `intro/crash` → `intro/3` opens the shutter |
| 2 | Explore, no card | Corridor footsteps echo (`tick/footsteps`); keypad denies with a hint; generator room hints "no fuse" |
| 3 | Has keycard | `event/got_key`: a stalker appears at the west end of the corridor and vanishes after you look at it; office door slams shut and candles go out |
| 4 | Containment opened | `event/k_scare_*`: lights flicker, the figure appears in the cell, then blackout and an elder guardian curse sound |
| 5 | Has fuse | — |
| 6 | Chase | `gen/1` all lights on → `gen/2` lockdown and alarm → `gen/3*` three bangs on the door → `gen/3c` blackout, red emergency lights (lit `deepslate_redstone_ore`), tunnels open, checkpoint set → `gen/4` Subject 9 (wither skeleton, speed 0.34, 100 damage, invulnerable) bursts in |
| 7 | Ending | `end/1` shutter closes → knocks → ride up B9–B1 → "ESCAPED" → lamp dies, sniff → jumpscare (camera forced to face it, roar) → "THE END" → time and deaths shown, "Play again" link |

The mirror scare works at any stage from 2 on. Look north into the washroom mirror and the figure stands in the reflected doorway behind you. Turn around and the mirror shatters.

### Systems
- **Lights**: redstone lamps set directly in the ceiling with `setblock ...[lit=true/false]`. There's no redstone behind them; with `randomTickSpeed 0` they keep their state. `build/lamps_backup` (dim start), `lamps_all_on`, `lamps_all_off`. C2 flickers randomly.
- **Emergency lights**: 46 `deepslate_redstone_ore` blocks in the walls at y43. They look like red-flecked stone until the chase, then they're set to `lit=true` (red glow, light level 9).
- **Chase leash**: every 10 ticks a marker is dropped at the player. If Subject 9 is more than 16 blocks away, it teleports to the marker from 3 seconds ago, so it never gets lost but a sprinting player can stay ahead.
- **Death**: `deathCount` objective. Immediate respawn at the generator checkpoint, and Subject 9 comes back after 100 ticks.
- **Effects**: camera shake (`fx/shake`, rotation jitter through tp), alarm, radio (tellraw plus a click sound).
- `start` = `reset` (clear every scheduled function, kill `@e[tag=s9]`, rebuild everything, reset scores, respawn keycard and fuse) + `intro/0`.

---

## 5. Lessons already learned (don't repeat these)

1. **Selector volumes (`dx/dy/dz`) match any hitbox that *touches* `[x, x+dx+1]`.** The first version triggered the ending while the player stood in the lift doorway. The shutter slammed shut on him, he died, and he "escaped" anyway. `box_selector()` now insets by the player's half-width (0.3), so triggers use the player's feet position. Anything that closes a door must also rescue a player standing in the doorway (see `DOORWAY_BOX` in `end/1`).
2. **1.20.4 specifics**: `data/<ns>/functions/` (plural), `tags/functions/load|tick.json`, item NBT `{id, Count, tag:{...}}`, sign NBT `front_text:{messages:[...]}`, attribute names `minecraft:generic.*`. `random value 1..N` and `return` exist.
3. **Scheduled functions run as the server at world spawn**, so use `@a` and absolute coordinates in them, never `@s`.
4. A function with **one bad command fails to load entirely**, silently in game. Always check the server log for `Failed to load function`.
5. `fill` is capped at 32,768 blocks. `fill()` in the generator splits automatically.
6. Chunks must be loaded before a build. The pack calls `forceload add -16 -16 79 47` on load, and `join` waits 40 ticks before starting.
7. **Wither skeletons are 2.4 blocks tall**, so every path Subject 9 uses must be 3 blocks tall, doorways included.
8. Glass panes and iron bars placed by commands need explicit `east=true,west=true` states, or they render as posts.
9. Doors: set the lower half, then the upper. Re-setting the lower half copies its state to the upper.
10. A sculk shrieker only gives Darkness if `doWardenSpawning` is true, and then it can spawn a real Warden. We keep it false, so the shrieker is sound only.
11. A `fill` that changes nothing reports 0. Don't use it to count blocks in tests; check specific blocks with `execute if block`.

---

## 6. The ticking: likely sources

The player said "could hear ticking which pissed me off". These are the candidates, most likely first:

1. **`fx/alarm`**: `block.note_block.bit` every 8 ticks for about 7 seconds during lockdown. That's a very tick-like beep.
2. **The sculk sensor in containment** at `(27,41,28)`. Its tendrils make a clicking sound every time the player moves nearby, and it can go on for a long time.
3. **`chase/pulse`**: `entity.warden.heartbeat` every 10 ticks while Subject 9 is within 12 blocks, plus `entity.warden.step` every 10 ticks. It's a steady metronome.
4. **Radio messages**: each one plays `ui.button.click` plus `note_block.bit`.
5. **Footstep echo** in the corridor: `block.deepslate_tiles.step` every 10 walked ticks.
6. **Lift ride**: `block.chain.step` plus `minecart.riding` every 30 ticks.

Default fix if the player can't say which: remove the sculk sensor, replace the alarm with a slow siren-like layered sound (or a custom one from the resource pack), make the heartbeat irregular and distance-based instead of a fixed 10-tick pulse, and drop the click from radio messages. **Nothing should repeat on a fixed short interval.**

---

## 7. Proposed expansion (confirm with the player first)

Target length is **25–35 minutes**, with a clear rise in tension across three acts.

### Act 0: a real introduction (on the surface, in daylight or storm)
- Open outside: a rainy night at a fenced surface facility (a small built area at the top of the shaft). Put Blindness only on the very first fade-in. The player should *see* where they are.
- A cutscene camera: put the player in spectator on a moving armor stand with `spectate`, or use tp steps. Title card, then Ops briefing on the radio with names, the mission, and the fact that the last team never came back.
- A walkable security hut with a sign-in sheet (the last entries are 41 days old), a bulletin board and a locker with your gear. This is a moment of normality before anything goes wrong.
- The lift ride down, where something *is on the roof of the lift* (footsteps and a scrape above you). Then the crash.

### Act 1: dread (explore, no direct threat)
- More space: two floors (B8 and B9, linked by stairs), and dorms, a cafeteria, a lab and a server room. Each room should have one memorable image.
- **A flashlight with a battery.** Hold a named item; while it's held, a `light` block follows a marker 3 blocks ahead of the player's eyes (raycast every tick), and the battery drains. Batteries are pickups. This is the biggest single improvement to dread, because darkness becomes a resource.
- A varied scare catalogue with no repeats: doors that open by themselves, a phone that rings, a radio voice that isn't Ops, a corridor that's different when you turn back (swap the geometry while it's out of view), objects moved between visits, a figure visible through a window that's gone when you enter.

### Act 2: hunted (Subject 9 roams)
- **"Only moves in the dark / when not seen"** mechanic (it's in the lore, so use it). Subject 9 roams between waypoints but freezes while the player looks at it *and* it's lit (flashlight counts). Look detection is a dot product or raycast from the eyes. When you look away or the light flickers, it moves closer. This is Weeping-Angel horror and it matches the story.
- **Hiding spots**: lockers (the player is tp'd inside, the view is restricted, breathing sounds). Subject 9 checks some of them.
- Sound as information: its footsteps are directional and irregular, so the player learns to listen.

### Act 3: escape
- Keep the generator twist ("the lights let it see you") but make the chase longer and **readable**: the red emergency route, a collapsing section, one wrong path that's a dead end with a locker to hide in.
- The ending has two outcomes depending on whether the player read all the logs or found Marsh. A secret ending is optional.

### Resource pack (strongly recommended)
- Custom sounds (`.ogg`): real ambience beds, a proper alarm, radio static, voice-like whispers, its footsteps.
- Fog and darker lighting through core shaders are fragile, so be careful; at minimum use a custom lightmap and texture tweaks.
- A retexture for Subject 9 (the wither skeleton texture) so it's a unique creature, not a recognisable mob.

---

## 8. How to test (required, and it's how the first version's bugs were caught)

1. Download the **official 1.20.4 server jar** from Mojang (`piston-meta.mojang.com/mc/game/version_manifest_v2.json` → 1.20.4 → `downloads.server`). The expected SHA-1 is `8dd1a28015f51b1803213892b50b7b4fc76e594d`. It needs Java 17+. Running it means accepting the Minecraft EULA (`eula=true`). **Confirm that with the player before you do it.**
2. `server.properties`: `level-type=minecraft\:flat`, void `generator-settings` (`{"layers":[{"block":"minecraft:air","height":1}],"biome":"minecraft:the_void","features":false}`), `enable-rcon=true`, `online-mode=false`, `gamemode=adventure`, `difficulty=normal`.
3. Put `Station9/` in `world/datapacks/`, start the server, and **grep the log for `Failed to load function`**. That must be zero.
4. Drive it over RCON: run `function station9:reset`, then `execute if block ...` and `execute if entity ...` checks after each event function, and simulate buttons and levers by `setblock`-ing them powered. A small Python RCON client is about 15 lines.
5. For hitbox and selector checks, summon a 0.6-wide mob (a zombie with NoAI) at test positions.
6. **You can't test player feel on a server with no player.** Tell the player plainly what you couldn't verify (chase difficulty, look detection, audio balance).

## 9. How to deliver

1. Reset to stage 0 (`function station9:reset`), `save-all flush`, `stop`.
2. `python3 package_world.py <server>/world "<out>/Station 9"`.
3. Zip it and give the player the zip. They unzip it into `~/Library/Application Support/minecraft/saves/`, then play on **1.20.4**.
4. Keep `generate.py` as the single source of truth, and update `README.md` and this brief.

## 10. Acceptance checklist
- [ ] Zero `Failed to load function` lines
- [ ] Nothing ticks or beeps on a fixed short loop
- [ ] A real introduction the player can walk around in
- [ ] 25–35 minutes, with at least one threat that roams before the finale
- [ ] No door or shutter can close on the player
- [ ] Every scare is different, and none repeats identically
- [ ] Restart (`/function station9:start`) fully resets everything
- [ ] Delivered as a ready-to-play 1.20.4 world zip
