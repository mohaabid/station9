playsound minecraft:entity.zombie.attack_iron_door hostile @a 48 42 20 1.6 0.6 1
playsound minecraft:entity.ravager.attack hostile @a 48 42 20 1.1199999999999999 0.5 1
scoreboard players set #shake s9 6
schedule function station9:fx/shake 1t
setblock 52 44 17 minecraft:redstone_lamp[lit=false]
setblock 52 44 23 minecraft:redstone_lamp[lit=false]
schedule function station9:gen/3c 16t
