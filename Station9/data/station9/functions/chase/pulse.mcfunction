scoreboard players set #ct s9 0
execute if score #hunter s9 matches 1 run function station9:chase/trail
execute at @e[tag=s9_hunter] run playsound minecraft:entity.warden.step hostile @a ~ ~ ~ 1.4 0.6
execute as @a at @s if entity @e[tag=s9_hunter,distance=..12] run playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 1 1.2
execute store result score #r s9 run random value 1..6
execute if score #r s9 matches 1 at @e[tag=s9_hunter] run playsound minecraft:entity.wither_skeleton.ambient hostile @a ~ ~ ~ 1.2 0.4
