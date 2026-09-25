function station9:reset
function station9:reset_entities
gamemode adventure @a
effect clear @a
effect give @a minecraft:saturation infinite 0 true
give @a minecraft:carrot_on_a_stick{s9light:1b,CustomModelData:9101,display:{Name:"{\"text\": \"Flashlight\", \"italic\": false, \"color\": \"white\"}",Lore:["{\"text\": \"Right-click: on / off\", \"color\": \"dark_gray\", \"italic\": false}"]}} 1
give @a minecraft:iron_nugget{s9batt:1b,CustomModelData:9102,display:{Name:"{\"text\": \"Battery\", \"italic\": false, \"color\": \"yellow\"}",Lore:["{\"text\": \"Swapped in automatically\", \"color\": \"dark_gray\", \"italic\": false}"]}} 2
scoreboard players set #kit s9 1
scoreboard players set #s_relay s9 1
scoreboard players set #s_code s9 1
scoreboard players set #s_release s9 1
fill 11 51 21 12 53 21 minecraft:air
fill 6 51 19 6 52 20 minecraft:air
function station9:build/lamps_off
function station9:build/b8_backup
scoreboard players set #stage s9 8
function station9:build/b9_backup
tp @a 52.5 41 20.5 -90 0
scoreboard players set #tab s9 1
fill 30 41 21 31 43 21 minecraft:air
function station9:gen/1
