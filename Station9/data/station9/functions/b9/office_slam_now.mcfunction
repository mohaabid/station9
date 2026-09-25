setblock 15 41 18 minecraft:dark_oak_door[facing=north,hinge=left,open=false,half=lower]
setblock 15 42 18 minecraft:dark_oak_door[facing=north,hinge=left,open=false,half=upper]
playsound minecraft:entity.zombie.attack_wooden_door hostile @a 15 42 18 1.2 0.8 0
playsound minecraft:block.wooden_door.close block @a 15 42 18 1 0.6 0
setblock 15 44 14 minecraft:redstone_lamp[lit=false]
schedule function station9:fx/on_o1 30t
effect give @a minecraft:darkness 3 0 true
