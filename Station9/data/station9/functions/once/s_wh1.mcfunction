scoreboard players set #s_wh1 s9 1
tellraw @a ["", {"text": "i can hear you", "color": "dark_gray", "italic": true}]
execute as @a at @s run playsound station9:voice.wh_hear voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 37
