scoreboard players set #teach s9 3
scoreboard players set #tw s9 0
setblock 33 44 19 minecraft:redstone_lamp[lit=false]
schedule function station9:fx/on_c3t 9t
setblock 45 44 20 minecraft:redstone_lamp[lit=false]
schedule function station9:fx/on_c4u 9t
tp @e[tag=s9_hunter] 37.5 41 20.0 90 0
scoreboard players set #hnode s9 5
scoreboard players set #hnext s9 -1
scoreboard players set #htarget s9 5
scoreboard players set #hwait s9 0
