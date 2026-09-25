scoreboard players set #stage s9 1
scoreboard players set #cam s9 0
function station9:cam/init
gamemode spectator @a
effect clear @a
effect give @a minecraft:saturation infinite 0 true
weather rain 1000000
time set 18000
function station9:story/opening
