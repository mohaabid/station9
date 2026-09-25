setblock 22 52 30 minecraft:polished_blackstone_button[face=floor,facing=north,powered=false]
execute if score #tapeon s9 matches 1.. run return 0
scoreboard players set #tapeon s9 320
execute if score #t_hale1 s9 matches 0 run scoreboard players add #tapes s9 1
scoreboard players set #t_hale1 s9 1
stopsound @a voice
tellraw @a ["", {"text": "[Tape] ", "color": "green"}, {"text": "Dr. Hale: ", "color": "green"}, {"text": "Hale. Day 115, 02:14. The power dipped for less than a second. When the lights came back, Subject 9 was pressed against the glass. It had been at the back wall. It only moves in the dark.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.tape_hale1 voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 320
