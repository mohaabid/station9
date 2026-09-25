scoreboard players set #steam s9 1
particle minecraft:campfire_signal_smoke 46.5 42.5 35.6 0.2 0.4 0.1 0.03 60 force
playsound minecraft:block.fire.extinguish block @a 46.5 42.5 35.5 1.3 0.6 1
playsound minecraft:entity.generic.extinguish_fire block @a 46.5 42.5 35.5 1.3 0.5 1
scoreboard players set #shake s9 4
schedule function station9:fx/shake 1t
