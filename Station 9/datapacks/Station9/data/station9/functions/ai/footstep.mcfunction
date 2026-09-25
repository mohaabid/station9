scoreboard players set #hdist s9 0
execute store result score #hstride s9 run random value 1300..2100
execute at @e[tag=s9_hunter] run playsound station9:sfx.step hostile @a ~ ~ ~ 1.4 1.0 0
