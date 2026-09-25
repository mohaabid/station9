scoreboard objectives add s9 dummy
scoreboard objectives add s9_id dummy
scoreboard objectives add s9_ln dummy
scoreboard objectives add s9_age dummy
scoreboard objectives add s9_walk minecraft.custom:minecraft.walk_one_cm
scoreboard objectives add s9_sprint minecraft.custom:minecraft.sprint_one_cm
scoreboard objectives add s9_click minecraft.used:minecraft.carrot_on_a_stick
scoreboard objectives add s9_deaths deathCount
scoreboard objectives add s9_bat dummy
scoreboard objectives add s9_hud dummy {"text":"STATION 9","color":"dark_red","bold":true}
scoreboard objectives modify s9_hud numberformat blank
scoreboard objectives setdisplay sidebar s9_hud
scoreboard players set #2 s9 2
scoreboard players set #5 s9 5
scoreboard players set #10 s9 10
scoreboard players set #20 s9 20
scoreboard players set #60 s9 60
scoreboard players set #100 s9 100
scoreboard players set #1000 s9 1000
scoreboard players set #36000 s9 36000
scoreboard players set #18000 s9 18000
scoreboard players set #-1 s9 -1
execute unless score #stage s9 = #stage s9 run scoreboard players set #stage s9 0
forceload add -16 -16 79 47
function station9:rules
