execute unless score #stage s9 matches 5..8 run return 0
execute if score #talk s9 matches 1.. run return run schedule function station9:line/wh_hear 20t
tellraw @a ["", {"text": "i can hear you", "color": "dark_gray", "italic": true}]
execute as @a at @s run playsound station9:voice.wh_hear voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 37
