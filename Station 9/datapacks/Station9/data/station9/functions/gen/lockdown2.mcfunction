stopsound @a voice
tellraw @a ["", {"text": "[PA] ", "color": "gold"}, {"text": "Station PA: ", "color": "gold"}, {"text": "Containment breach on level B9. Lockdown in effect.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a3_lockdown voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 158
