setblock 15 41 18 minecraft:dark_oak_door[facing=north,hinge=left,open=false,half=lower]
setblock 15 42 18 minecraft:dark_oak_door[facing=north,hinge=left,open=false,half=upper]
playsound minecraft:entity.zombie.attack_wooden_door hostile @a 15 42 18 1.2 0.8 1
playsound minecraft:block.wooden_door.close block @a 15 42 18 1 0.6 1
setblock 16 42 11 minecraft:candle[candles=3,lit=false]
setblock 11 41 17 minecraft:white_candle[candles=4,lit=false]
setblock 20 42 13 minecraft:red_candle[candles=1,lit=false]
execute as @a at @s run playsound minecraft:block.candle.extinguish block @s ~ ~ ~ 1 0.8
effect give @a minecraft:darkness 3 0 true
