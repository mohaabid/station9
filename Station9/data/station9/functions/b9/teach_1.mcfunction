scoreboard players set #teach s9 2
scoreboard players set #tw s9 0
setblock 45 44 20 minecraft:redstone_lamp[lit=false]
schedule function station9:fx/on_c4t 9t
tp @e[tag=s9_hunter] 43.5 41 20.0 90 0
scoreboard players set #hnode s9 6
scoreboard players set #hnext s9 -1
scoreboard players set #htarget s9 6
scoreboard players set #hwait s9 0
