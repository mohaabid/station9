# roughly one distant noise every 20 seconds
execute store result score #r s9 run random value 1..2000
execute if score #r s9 matches 1 at @a run playsound minecraft:ambient.cave ambient @a ~ ~ ~ 0.8 0.8
execute if score #r s9 matches 2 at @a run playsound minecraft:block.iron_door.close hostile @a ~12 ~ ~6 1 0.6
execute if score #r s9 matches 3 at @a run playsound minecraft:entity.warden.heartbeat hostile @a ~ ~ ~ 0.5 0.7
execute if score #r s9 matches 4 at @a run playsound minecraft:block.chain.step hostile @a ~-8 ~2 ~-8 1 0.5
execute if score #r s9 matches 5 at @a run playsound minecraft:entity.wither_skeleton.ambient hostile @a ~-10 ~ ~10 0.5 0.5
execute if score #r s9 matches 6 at @a run playsound minecraft:block.sculk_shrieker.shriek hostile @a ~15 ~ ~-10 0.4 0.6
