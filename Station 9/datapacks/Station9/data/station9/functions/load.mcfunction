scoreboard objectives add s9 dummy
scoreboard objectives add s9_walk minecraft.custom:minecraft.walk_one_cm
scoreboard objectives add s9_sprint minecraft.custom:minecraft.sprint_one_cm
scoreboard objectives add s9_deaths deathCount
scoreboard objectives add s9_age dummy
scoreboard objectives add s9_fs dummy
scoreboard objectives add s9_idle dummy
scoreboard players set #2 s9 2
scoreboard players set #20 s9 20
scoreboard players set #60 s9 60
execute unless score #stage s9 = #stage s9 run scoreboard players set #stage s9 0
forceload add -16 -16 79 47
function station9:rules
