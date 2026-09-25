stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Why did your light go out? ...Oh. Oh God. It's on the roof. Don't move. Don't make a sound.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.e_dark voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 125
