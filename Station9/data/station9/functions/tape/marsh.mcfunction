setblock 11 42 1 minecraft:polished_blackstone_button[face=floor,facing=north,powered=false]
execute if score #tapeon s9 matches 1.. run return 0
scoreboard players set #tapeon s9 281
execute if score #t_marsh s9 matches 0 run scoreboard players add #tapes s9 1
scoreboard players set #t_marsh s9 1
stopsound @a voice
tellraw @a ["", {"text": "[Tape] ", "color": "green"}, {"text": "M. Marsh: ", "color": "green"}, {"text": "This is Marsh. If you can hear this, don't start the generator. It turns every light on at once, and then it sees everything. ...If you have to, and you make it to the lift, kill the cage light before you go up. It rides on the roof. It can't find you in the dark.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.tape_marsh voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 281
