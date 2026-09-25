execute if score #teach s9 matches 4 run return 0
scoreboard players set #teach s9 4
setblock 33 44 19 minecraft:redstone_lamp[lit=false]
schedule function station9:fx/on_c3u 12t
setblock 45 44 20 minecraft:redstone_lamp[lit=false]
schedule function station9:fx/on_c4v 12t
setblock 21 44 20 minecraft:redstone_lamp[lit=false]
schedule function station9:fx/on_c2t 12t
playsound station9:sfx.step hostile @a 40 41 20 1.4 0.9 0
tp @e[tag=s9_hunter] 52.0 41 16.5
scoreboard players set #hnode s9 32
scoreboard players set #hnext s9 -1
scoreboard players set #htarget s9 32
scoreboard players set #hwait s9 0
scoreboard players set #hmode s9 1
scoreboard players set #hspd s9 55
scoreboard players set #hgrace s9 400
function station9:ai/roam
function station9:story/rule
schedule function station9:story/lockers_line 954t
