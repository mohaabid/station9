playsound minecraft:entity.zombie.attack_iron_door hostile @a 7 42 20 1.8 0.5 1
scoreboard players set #shake s9 5
schedule function station9:fx/shake 1t
scoreboard players set #ride s9 10
schedule function station9:end/ride 25t
