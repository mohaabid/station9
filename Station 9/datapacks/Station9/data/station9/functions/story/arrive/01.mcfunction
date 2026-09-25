stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "The gate's been open since the evacuation. Head for the security hut, sign in, then grab the contractor kit from the locker.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_gate voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 149
