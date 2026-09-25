"""Subject 9.

It walks a graph of waypoints (world.NODES / world.EDGES) by teleporting in small steps,
so it can never get stuck or lost. Routes are precomputed here in Python for every door
state (world.TABLES) and stored as next-hop tables in command storage.

Rules the player learns:
  * While you look at it and it is lit (a lamp, or your flashlight), it cannot move.
  * It can't see in the dark. It finds you by sound (sprinting carries, sneaking is silent)
    or by light (your flashlight, or standing under a lamp) when it has line of sight.
  * Lockers hide you. If it saw you get in, it waits outside. Don't come out.

Modes (#hmode): 0 off, 1 wander, 2 investigate a noise, 3 hunt, 4 check a locker, 5 chase, 6 statue
"""
import heapq
import math

from . import world as W
from .mc import NS, call, fn, fmt, sched, snd

NODE_IDS = {name: i for i, name in enumerate(W.NODES)}

# Speeds in thousandths of a block per tick (walking is ~216, sprinting ~280)
SPEED = {"wander": 55, "investigate": 95, "hunt": 115, "lunge": 215, "check": 90,
         "chase": 232, "chase_far": 300, "chase_watched": 55}
LUNGE_RANGE = 6
HUNT_GIVE_UP = 160          # ticks without sight before it goes back to searching
CHECK_TICKS = 130           # how long it stands outside a locker
CATCH_RANGE = 1.3


def dist(a, b):
    return math.dist(W.NODES[a], W.NODES[b])


def next_hops(open_doors):
    names = list(W.NODES)
    adj = {n: [] for n in names}
    for e in W.EDGES:
        a, b = e[0], e[1]
        door = e[2] if len(e) > 2 else None
        if door is None or door in open_doors:
            adj[a].append(b)
            adj[b].append(a)
    table = []
    for src in names:
        # Dijkstra from src, remembering the first hop
        best = {src: 0.0}
        first = {src: -1}
        pq = [(0.0, src, None)]
        while pq:
            d, n, f = heapq.heappop(pq)
            if d > best.get(n, 1e9):
                continue
            for m in adj[n]:
                nd = d + dist(n, m)
                if nd < best.get(m, 1e9) - 1e-9:
                    best[m] = nd
                    first[m] = NODE_IDS[m] if n == src else first[n]
                    heapq.heappush(pq, (nd, m, None))
        row = [first.get(dst, -1) if dst != src else NODE_IDS[src] for dst in names]
        table.append(row)
    return table


def nearest_node(p, level_y):
    cands = [n for n, q in W.NODES.items() if abs(q[1] - level_y) < 3]
    return min(cands, key=lambda n: math.dist((p[0] + .5, p[2] + .5), (W.NODES[n][0], W.NODES[n][2])))


def place(node, yaw=None):
    """Put it on a node, standing still."""
    x, y, z = W.NODES[node]
    rot = f" {yaw} 0" if yaw is not None else ""
    return [f"tp @e[tag=s9_hunter] {fmt(x)} {y} {fmt(z)}{rot}",
            f"scoreboard players set #hnode s9 {NODE_IDS[node]}",
            "scoreboard players set #hnext s9 -1",
            f"scoreboard players set #htarget s9 {NODE_IDS[node]}",
            "scoreboard players set #hwait s9 0"]


def summon(node, yaw=0):
    x, y, z = W.NODES[node]
    return ["kill @e[tag=s9_hunter]",
            f'summon minecraft:wither_skeleton {fmt(x)} {y} {fmt(z)} {{Tags:["s9","s9_hunter"],NoAI:1b,Silent:1b,'
            f'Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",'
            f'HandItems:[{{}},{{}}],ArmorItems:[{{}},{{}},{{}},{{}}],Rotation:[{yaw}f,0f]}}'] + place(node, yaw)


def mode(m, speed=None):
    out = [f"scoreboard players set #hmode s9 {m}"]
    if speed:
        out.append(f"scoreboard players set #hspd s9 {SPEED[speed]}")
    return out


def target(node):
    return [f"scoreboard players set #htarget s9 {NODE_IDS[node]}", call("ai/retarget")]


def entities():
    """Markers the AI needs: one per node, one per locker, plus helpers."""
    out = []
    for name, (x, y, z) in W.NODES.items():
        i = NODE_IDS[name]
        out += [f'summon minecraft:marker {fmt(x)} {y} {fmt(z)} {{Tags:["s9","s9_node","s9n{i}"]}}',
                f"scoreboard players set @e[tag=s9n{i},limit=1] s9_id {i}"]
    for i, (p, facing) in enumerate(W.LOCKERS):
        x, y, z = p
        ln = NODE_IDS[nearest_node(p, y)]
        out += [f'summon minecraft:marker {x + .5} {y} {z + .5} {{Tags:["s9","s9_locker","s9l{i}"]}}',
                f"scoreboard players set @e[tag=s9l{i},limit=1] s9_id {i}",
                f"scoreboard players set @e[tag=s9l{i},limit=1] s9_ln {ln}"]
    out += ['summon minecraft:marker 0.5 -60 0.5 {Tags:["s9","s9_lp"]}',
            'summon minecraft:marker 0.5 -60 0.5 {Tags:["s9","s9_aim"]}']
    return out


def storage():
    out = []
    for t, doors in W.TABLES.items():
        rows = next_hops(doors)
        body = ",".join("[I;" + ",".join(str(v) for v in row) + "]" for row in rows)
        out.append(f"data modify storage {NS}:ai r{t} set value [{body}]")
    return out


def roam_pick(nodes, name):
    out = [f"execute store result score #r s9 run random value 0..{len(nodes) - 1}"]
    out += [f"execute if score #r s9 matches {i} run scoreboard players set #htarget s9 {NODE_IDS[n]}"
            for i, n in enumerate(nodes)]
    out.append(call("ai/retarget"))
    fn(name, out)
    return call(name)


def build():
    fn("ai/init", storage())

    # --- the loop --------------------------------------------------------------------------
    fn("ai/tick",
       "execute unless entity @e[tag=s9_hunter] run return 0",
       "scoreboard players add #e s9 1",
       "scoreboard players operation #e5 s9 = #e s9",
       "scoreboard players operation #e5 s9 %= #5 s9",
       f"execute if score #e5 s9 matches 0 as @a[limit=1] at @s as @e[tag=s9_node,sort=nearest,limit=1] "
       "run scoreboard players operation #pnode s9 = @s s9_id",
       call("ai/sense"),
       call("ai/think"),
       f"execute if score #hmode s9 matches 4 if score #lkphase s9 matches 1 if score #frozen s9 matches 0 run {call('ai/lk_approach')}",
       f"execute if score #hwait s9 matches 1 run {call('ai/after')}",
       "execute if score #hwait s9 matches 1.. run scoreboard players remove #hwait s9 1",
       f"execute if score #frozen s9 matches 0 if score #hwait s9 matches 0 if score #hnext s9 matches 0.. "
       f"if score #hgrace s9 matches ..0 run {call('ai/step')}",
       f"execute if score #frozen s9 matches 0 if score #hwait s9 matches 0 if score #hnext s9 matches ..-1 "
       f"if score #hgrace s9 matches ..0 if score #hmode s9 matches 3..5 unless score #hmode s9 matches 4 run {call('ai/approach')}",
       "execute if score #hgrace s9 matches 1.. run scoreboard players remove #hgrace s9 1",
       call("ai/catchcheck"),
       call("ai/presence"))

    # --- senses ------------------------------------------------------------------------------
    fn("ai/sense",
       "scoreboard players set #cand s9 0",
       "scoreboard players set #los s9 0",
       "scoreboard players set #lit s9 0",
       f"execute as @a[tag=!s9_hidden,limit=1] at @s if entity @e[tag=s9_hunter,distance=..44] anchored eyes "
       f"facing entity @e[tag=s9_hunter,limit=1] eyes run {call('ai/sense_p')}",
       f"execute at @e[tag=s9_hunter] positioned ~ ~1.2 ~ if predicate {NS}:lit run scoreboard players set #lit s9 1",
       "execute if score #beam s9 matches 1 run scoreboard players set #lit s9 1",
       "scoreboard players operation #wasw s9 = #watched s9",
       "scoreboard players set #watched s9 0",
       "execute if score #cand s9 matches 1 if score #los s9 matches 1 if score #lit s9 matches 1 run scoreboard players set #watched s9 1",
       "scoreboard players set #frozen s9 0",
       "execute if score #watched s9 matches 1 if score #hmode s9 matches 1..4 run scoreboard players set #frozen s9 1",
       "execute if score #hmode s9 matches 6 run scoreboard players set #frozen s9 1",
       "execute if score #watched s9 matches 1 run scoreboard players add #wtime s9 1",
       "# seeing you: line of sight, and you carry a light or stand in one",
       "scoreboard players set #sees s9 0",
       "execute if score #los s9 matches 1 if score #on s9 matches 1 run scoreboard players set #sees s9 1",
       f"execute if score #los s9 matches 1 as @a[tag=!s9_hidden] at @s if predicate {NS}:bright run scoreboard players set #sees s9 1",
       f"execute if score #watched s9 matches 1 if score #wasw s9 matches 0 run {call('ai/noticed')}",
       "# how long since it last had you in sight (it remembers you ducking into a locker)",
       "scoreboard players add #seenago s9 1",
       "execute if score #los s9 matches 1 run scoreboard players set #seenago s9 0")

    fn("ai/sense_p",
       "tp @e[tag=s9_aim,limit=1] ~ ~ ~ ~ ~",
       "execute store result score #ay s9 run data get entity @e[tag=s9_aim,limit=1] Rotation[0] 100",
       "execute store result score #ap s9 run data get entity @e[tag=s9_aim,limit=1] Rotation[1] 100",
       "execute store result score #py s9 run data get entity @s Rotation[0] 100",
       "execute store result score #pp s9 run data get entity @s Rotation[1] 100",
       "scoreboard players operation #ay s9 -= #py s9",
       "scoreboard players operation #ay s9 %= #36000 s9",
       "execute if score #ay s9 matches 18000.. run scoreboard players remove #ay s9 36000",
       "scoreboard players operation #ap s9 -= #pp s9",
       "execute if score #ay s9 matches -5200..5200 if score #ap s9 matches -4200..4200 run scoreboard players set #cand s9 1",
       "scoreboard players set #rs s9 0",
       call("ai/los_ray"))

    fn("ai/los_ray",
       "scoreboard players add #rs s9 1",
       "execute positioned ~ ~-2.1 ~ if entity @e[tag=s9_hunter,distance=..0.9] run return run scoreboard players set #los s9 1",
       f"execute unless block ~ ~ ~ #{NS}:see_through run return 0",
       "execute if score #rs s9 matches 88.. run return 0",
       f"execute positioned ^ ^ ^0.5 run {call('ai/los_ray')}")

    fn("ai/noticed",
       "# you just caught sight of it: a sting if it's close and it's been a while",
       "execute if score #stingcd s9 matches 1.. run return 0",
       f"execute as @e[tag=s9_hunter] at @s if entity @a[distance=..12] run {call('ai/sting')}")
    fn("ai/sting",
       "scoreboard players set #stingcd s9 1200",
       "execute as @a at @s run playsound station9:sfx.sting_dread master @s ~ ~ ~ 0.55 1")

    # --- decisions ------------------------------------------------------------------------------
    fn("ai/think",
       "execute if score #stingcd s9 matches 1.. run scoreboard players remove #stingcd s9 1",
       f"execute if score #sees s9 matches 1 if score #hmode s9 matches 1..2 run {call('ai/spotted')}",
       f"execute if score #hmode s9 matches 3 run {call('ai/hunt')}",
       f"execute if score #hmode s9 matches 5 run {call('ai/chase')}")

    fn("ai/spotted",
       mode(3, "hunt"),
       "scoreboard players set #lost s9 0",
       "scoreboard players set #hwait s9 0",
       "scoreboard players operation #htarget s9 = #pnode s9",
       call("ai/retarget"))

    fn("ai/hunt",
       "execute if score #sees s9 matches 1 run scoreboard players set #lost s9 0",
       "execute if score #sees s9 matches 0 run scoreboard players add #lost s9 1",
       f"execute if score #lost s9 matches 0 if score #e5 s9 matches 0 unless score #htarget s9 = #pnode s9 run {call('ai/to_player')}",
       f"scoreboard players set #hspd s9 {SPEED['hunt']}",
       f"execute as @e[tag=s9_hunter] at @s if entity @a[tag=!s9_hidden,distance=..{LUNGE_RANGE}] run scoreboard players set #hspd s9 {SPEED['lunge']}",
       f"execute if score #lost s9 matches {HUNT_GIVE_UP}.. run {call('ai/give_up')}")
    fn("ai/to_player", "scoreboard players operation #htarget s9 = #pnode s9", call("ai/retarget"))
    fn("ai/give_up", mode(2, "investigate"), "scoreboard players set #lost s9 0")

    fn("ai/chase",
       f"execute if score #e5 s9 matches 0 unless score #htarget s9 = #pnode s9 if entity @a[tag=!s9_hidden] run {call('ai/to_player')}",
       f"scoreboard players set #hspd s9 {SPEED['chase']}",
       f"execute as @e[tag=s9_hunter] at @s unless entity @a[distance=..20] run scoreboard players set #hspd s9 {SPEED['chase_far']}",
       f"execute if score #watched s9 matches 1 run scoreboard players set #hspd s9 {SPEED['chase_watched']}")

    fn("ai/heard",
       "# a noise: go and look",
       "execute if score #hmode s9 matches 4..6 run return 0",
       "execute if score #hgrace s9 matches 1.. run return 0",
       f"execute if score #hmode s9 matches 1..2 run {call('ai/heard_go')}",
       "execute if score #hmode s9 matches 3 run scoreboard players set #lost s9 0",
       f"execute if score #hmode s9 matches 3 run {call('ai/to_player')}")
    fn("ai/heard_go",
       "execute if score #hmode s9 matches 2 if score #htarget s9 = #pnode s9 run return 0",
       mode(2, "investigate"),
       "scoreboard players set #hwait s9 0",
       "scoreboard players operation #htarget s9 = #pnode s9",
       call("ai/retarget"),
       f"execute if score #s_heard s9 matches 0 if score #talk s9 matches ..0 run {call('story/heard_hint')}")

    fn("ai/hid",
       "# you got into a locker",
       f"execute if score #hmode s9 matches 3 if score #seenago s9 matches ..40 run return run {call('ai/check_locker')}",
       f"execute if score #hmode s9 matches 5 if score #seenago s9 matches ..40 run return run {call('ai/check_locker')}",
       f"execute if score #hmode s9 matches 3 run return run {call('ai/lost_you')}",
       f"execute if score #hmode s9 matches 5 run return run {call('ai/lost_you')}")
    fn("ai/check_locker",
       mode(4, "check"),
       "scoreboard players set #hwait s9 0",
       "scoreboard players set #lkphase s9 0",
       "tag @e[tag=s9_lkt] remove s9_lkt",
       "execute as @a[tag=s9_hidden] at @s align xyz positioned ~.5 ~ ~.5 as @e[tag=s9_locker,distance=..0.3] run tag @s add s9_lkt",
       "scoreboard players operation #htarget s9 = #lk s9",
       call("ai/retarget"))
    fn("ai/lost_you",
       mode(2, "investigate"),
       "scoreboard players set #hwait s9 0",
       "scoreboard players operation #htarget s9 = #pnode s9",
       call("ai/retarget"))

    # arrival at the end of a route
    fn("ai/arrived",
       f"execute if score #hmode s9 matches 1 run {call('ai/arr_wander')}",
       f"execute if score #hmode s9 matches 2 run {call('ai/arr_search')}",
       f"execute if score #hmode s9 matches 4 run {call('ai/arr_locker')}")
    fn("ai/arr_wander",
       "execute store result score #hwait s9 run random value 30..150",
       call("ai/roam"))
    fn("ai/arr_search",
       "scoreboard players set #hwait s9 90",
       f"execute at @e[tag=s9_hunter] run {snd('sfx.sniff', ('~', '~1.6', '~'), 1.0, 0.9)}")
    fn("ai/arr_locker", "scoreboard players set #lkphase s9 1")
    fn("ai/lk_approach",
       "# walk the last few steps right up to the locker door",
       f"execute as @e[tag=s9_hunter] at @s unless entity @e[tag=s9_lkt,distance=..1.25] facing entity @e[tag=s9_lkt,limit=1] feet "
       "run return run tp @s ^ ^ ^0.08 ~ 0",
       "scoreboard players set #lkphase s9 2",
       call("ai/lk_wait"))
    fn("ai/lk_wait",
       f"scoreboard players set #hwait s9 {CHECK_TICKS}",
       "execute as @e[tag=s9_hunter] at @s run tp @s ~ ~ ~ facing entity @e[tag=s9_lkt,limit=1] feet",
       "execute as @e[tag=s9_hunter] at @s run tp @s ~ ~ ~ ~ 0",
       f"execute at @e[tag=s9_hunter] run {snd('sfx.sniff', ('~', '~1.6', '~'), 1.2, 0.8)}",
       f"{sched('ai/locker_breath', 40)}")
    fn("ai/locker_breath",
       "execute unless score #hmode s9 matches 4 run return 0",
       f"execute at @e[tag=s9_hunter] run {snd('sfx.breath', ('~', '~1.8', '~'), 1.2, 0.8)}",
       "execute at @e[tag=s9_hunter] run playsound station9:sfx.locker_close block @a ~ ~ ~ 0.4 0.6")

    fn("ai/after",
       "# a pause just ended",
       f"execute if score #hmode s9 matches 2 run {call('ai/back_to_wander')}",
       f"execute if score #hmode s9 matches 4 run {call('ai/done_locker')}")
    fn("ai/back_to_wander", mode(1, "wander"), call("ai/roam"))
    fn("ai/done_locker",
       f"execute if score #stage s9 matches 9 run return run {call('ai/done_locker_chase')}",
       mode(1, "wander"), call("ai/roam"))
    fn("ai/done_locker_chase",
       "# it gives up on the locker and goes back the way it came; the chase resumes when you move",
       mode(2, "investigate"),
       f"scoreboard players set #htarget s9 {NODE_IDS['c48']}",
       call("ai/retarget"),
       f"{sched('chase/resume', 140)}")

    fn("ai/roam",
       f"execute if score #tab s9 matches 0 run return run {call('ai/roam0')}",
       roam_pick(W.ROAM + W.ROAM_CONTAINED, "ai/roam1"))
    roam_pick(W.ROAM, "ai/roam0")

    # --- movement ---------------------------------------------------------------------------------
    fn("ai/retarget",
       "# idle on a node: route now. Otherwise the next node recomputes the route on arrival.",
       f"execute if score #hnext s9 matches ..-1 run {call('ai/route')}")

    fn("ai/route",
       "execute store result storage station9:ai q.t int 1 run scoreboard players get #tab s9",
       "execute store result storage station9:ai q.a int 1 run scoreboard players get #hnode s9",
       "execute store result storage station9:ai q.b int 1 run scoreboard players get #htarget s9",
       "function station9:ai/route_m with storage station9:ai q",
       "execute if score #hnext s9 = #hnode s9 run scoreboard players set #hnext s9 -1",
       "tag @e[tag=s9_next] remove s9_next",
       "execute as @e[tag=s9_node] if score @s s9_id = #hnext s9 run tag @s add s9_next")
    fn("ai/route_m", "$execute store result score #hnext s9 run data get storage station9:ai r$(t)[$(a)][$(b)]")

    fn("ai/step",
       "execute store result storage station9:ai m.spd double 0.001 run scoreboard players get #hspd s9",
       "function station9:ai/move with storage station9:ai m",
       "scoreboard players operation #hdist s9 += #hspd s9",
       f"execute if score #hdist s9 >= #hstride s9 run {call('ai/footstep')}")
    fn("ai/move",
       f"$execute as @e[tag=s9_hunter,limit=1] at @s if entity @e[tag=s9_next,distance=..$(spd)] run return run {call('ai/snap')}",
       "$execute as @e[tag=s9_hunter,limit=1] at @s facing entity @e[tag=s9_next,limit=1] feet run tp @s ^ ^ ^$(spd) ~ 0")
    fn("ai/snap",
       "execute at @e[tag=s9_next,limit=1] run tp @e[tag=s9_hunter] ~ ~ ~",
       "scoreboard players operation #hnode s9 = #hnext s9",
       "scoreboard players set #hnext s9 -1",
       f"execute if score #hnode s9 = #htarget s9 run return run {call('ai/arrived')}",
       call("ai/route"))

    fn("ai/approach",
       "# at the end of its route and you're right there: straight at you",
       "execute unless score #los s9 matches 1 unless score #hmode s9 matches 5 run return 0",
       "execute as @e[tag=s9_hunter] at @s unless entity @a[tag=!s9_hidden,distance=..10] run return 0",
       "execute store result storage station9:ai m.spd double 0.001 run scoreboard players get #hspd s9",
       "function station9:ai/approach_m with storage station9:ai m",
       "scoreboard players operation #hdist s9 += #hspd s9",
       f"execute if score #hdist s9 >= #hstride s9 run {call('ai/footstep')}")
    fn("ai/approach_m",
       "$execute as @e[tag=s9_hunter,limit=1] at @s facing entity @a[tag=!s9_hidden,limit=1,sort=nearest] feet "
       "run tp @s ^ ^ ^$(spd) ~ 0")

    fn("ai/footstep",
       "scoreboard players set #hdist s9 0",
       "execute store result score #hstride s9 run random value 1300..2100",
       f"execute at @e[tag=s9_hunter] run {snd('sfx.step', ('~', '~', '~'), 1.4, 1.0)}")

    fn("ai/presence",
       "# now and then, a breath in the dark",
       f"execute if score #hwait s9 matches 1.. if predicate {NS}:chance_1 at @e[tag=s9_hunter] run "
       + snd('sfx.breath', ('~', '~1.8', '~'), 1.1, 0.9))

    # --- catching you ---------------------------------------------------------------------------------
    fn("ai/catchcheck",
       "execute if score #hgrace s9 matches 1.. run return 0",
       "execute if score #catching s9 matches 1 run return 0",
       "execute if score #frozen s9 matches 1 run return 0",
       f"execute as @e[tag=s9_hunter] at @s if entity @a[tag=!s9_hidden,gamemode=adventure,distance=..{CATCH_RANGE}] run {call('ai/catch')}")
    fn("ai/catch",
       "scoreboard players set #catching s9 1",
       "effect give @a minecraft:slowness 2 255 true",
       "effect give @a minecraft:jump_boost 2 200 true",
       "execute as @a at @s run tp @s ~ ~ ~ facing entity @e[tag=s9_hunter,limit=1] eyes",
       "execute as @a at @s rotated ~ 0 positioned ^ ^ ^1.0 run tp @e[tag=s9_hunter] ~ ~ ~ facing entity @a[limit=1] feet",
       "execute as @e[tag=s9_hunter] at @s run tp @s ~ ~ ~ ~ 0",
       "execute as @a at @s run playsound station9:sfx.scream hostile @s ~ ~ ~ 1 1",
       "execute as @a at @s run playsound station9:sfx.sting_hit master @s ~ ~ ~ 0.9 1",
       sched("ai/catch2", 14))
    fn("ai/catch2",
       "effect give @a minecraft:blindness 3 0 true",
       "kill @a[gamemode=adventure]",
       "scoreboard players set #catching s9 0")

    fn("ai/respawned",
       "# you're back at the checkpoint; it goes somewhere far away and waits",
       f"scoreboard players set #hgrace s9 160",
       mode(1, "wander"),
       f"execute if score #stage s9 matches 5..6 run {call('ai/far_west')}",
       f"execute if score #stage s9 matches 7..8 run {call('ai/far_east')}",
       f"execute if score #s_caught s9 matches 0 run {sched('story/caught_line', 60)}")
    fn("ai/far_west", place("gne"), call("ai/roam"))
    fn("ai/far_east", place("recc"), call("ai/roam"))
