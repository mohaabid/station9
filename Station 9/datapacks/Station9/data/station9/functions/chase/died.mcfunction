scoreboard players set @s s9_deaths 0
scoreboard players add #deaths s9 1
scoreboard players set #hunter s9 0
tp @e[tag=s9_hunter] 0 -200 0
kill @e[tag=s9_hunter]
kill @e[tag=s9_trail]
effect give @a minecraft:darkness 5 0 true
title @a times 10 60 20
title @a title {"text": " "}
title @a subtitle {"text": "It lets you go. For now.", "color": "dark_red"}
schedule function station9:chase/release 100t
