stopsound @a voice
tellraw @a ["", {"text": "[PA] ", "color": "gold"}, {"text": "Station PA: ", "color": "gold"}, {"text": "Communications relay online. Backup power at eight percent.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_relay voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 165
