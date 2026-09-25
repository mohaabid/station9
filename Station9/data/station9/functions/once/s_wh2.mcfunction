scoreboard players set #s_wh2 s9 1
tellraw @a ["", {"text": "turn it off", "color": "dark_gray", "italic": true}]
execute as @a at @s run playsound station9:voice.wh_off voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 33
