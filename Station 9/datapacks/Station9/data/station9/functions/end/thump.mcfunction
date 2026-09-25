# it's on the roof. Is your light on?
execute as @a at @s run playsound station9:sfx.roof_thump hostile @s ~ ~3 ~ 1 1
scoreboard players set #shake s9 10
schedule function station9:fx/shake 1t
execute if block 5 52 18 minecraft:lever[powered=true] run return run function station9:end/b
function station9:end/a
