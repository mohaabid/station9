scoreboard players set #cand s9 0
scoreboard players set #los s9 0
scoreboard players set #lit s9 0
execute as @a[tag=!s9_hidden,limit=1] at @s if entity @e[tag=s9_hunter,distance=..44] anchored eyes facing entity @e[tag=s9_hunter,limit=1] eyes run function station9:ai/sense_p
execute at @e[tag=s9_hunter] positioned ~ ~1.2 ~ if predicate station9:lit run scoreboard players set #lit s9 1
execute if score #beam s9 matches 1 run scoreboard players set #lit s9 1
scoreboard players operation #wasw s9 = #watched s9
scoreboard players set #watched s9 0
execute if score #cand s9 matches 1 if score #los s9 matches 1 if score #lit s9 matches 1 run scoreboard players set #watched s9 1
scoreboard players set #frozen s9 0
execute if score #watched s9 matches 1 if score #hmode s9 matches 1..4 run scoreboard players set #frozen s9 1
execute if score #hmode s9 matches 6 run scoreboard players set #frozen s9 1
execute if score #watched s9 matches 1 run scoreboard players add #wtime s9 1
# seeing you: line of sight, and you carry a light or stand in one
scoreboard players set #sees s9 0
execute if score #los s9 matches 1 if score #on s9 matches 1 run scoreboard players set #sees s9 1
execute if score #los s9 matches 1 as @a[tag=!s9_hidden] at @s if predicate station9:bright run scoreboard players set #sees s9 1
execute if score #watched s9 matches 1 if score #wasw s9 matches 0 run function station9:ai/noticed
# how long since it last had you in sight (it remembers you ducking into a locker)
scoreboard players add #seenago s9 1
execute if score #los s9 matches 1 run scoreboard players set #seenago s9 0
