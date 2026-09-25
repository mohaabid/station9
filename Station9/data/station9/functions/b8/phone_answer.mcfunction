setblock 46 52 4 minecraft:stone_button[face=wall,facing=south,powered=false]
execute unless score #s_ring s9 matches 1 run return 0
execute if score #s_answered s9 matches 1 run return 0
scoreboard players set #s_answered s9 1
stopsound @a block station9:sfx.phone_ring
execute as @a at @s run playsound station9:sfx.phone_up master @s ~ ~ ~ 0.9 1.0
function station9:story/phone
