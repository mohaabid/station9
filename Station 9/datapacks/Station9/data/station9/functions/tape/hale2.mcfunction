setblock 31 42 10 minecraft:polished_blackstone_button[face=floor,facing=north,powered=false]
execute if score #tapeon s9 matches 1.. run return 0
scoreboard players set #tapeon s9 283
execute if score #t_hale2 s9 matches 0 run scoreboard players add #tapes s9 1
scoreboard players set #t_hale2 s9 1
stopsound @a voice
tellraw @a ["", {"text": "[Tape] ", "color": "green"}, {"text": "Dr. Hale: ", "color": "green"}, {"text": "Hale. Day 121. Marsh is gone. His keycard was on my desk this morning. I didn't put it there. ...It isn't afraid of the light. It just can't see in the dark. So it listens.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.tape_hale2 voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 283
