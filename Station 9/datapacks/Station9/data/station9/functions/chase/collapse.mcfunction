tp @a[x=38.3,y=51,z=16.3,dx=4.4,dy=2,dz=0.4] 45 51 17
fill 38 51 16 43 53 17 minecraft:cobbled_deepslate
fill 38 53 16 43 53 17 minecraft:gravel
setblock 43 51 16 minecraft:cobbled_deepslate_stairs[facing=east]
setblock 43 52 17 minecraft:air
setblock 38 52 16 minecraft:air
particle minecraft:campfire_cosy_smoke 42 52 17 1.5 1 0.5 0.02 80 force
particle minecraft:block minecraft:gravel 42 53 17 2 0.5 0.5 1 120 force
execute as @a at @s run playsound station9:sfx.collapse block @s ~ ~ ~ 1 1
scoreboard players set #shake s9 14
schedule function station9:fx/shake 1t
scoreboard players set #tab s9 3
scoreboard players set #hnext s9 -1
function station9:ai/route
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "The hall's coming down! Through the cafeteria!", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a3_collapse voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 55
