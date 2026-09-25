scoreboard players set #cstalk s9 2
setblock 10 44 19 minecraft:redstone_lamp[lit=false]
tp @e[tag=s9_cstalk] 0 -200 0
kill @e[tag=s9_cstalk]
playsound minecraft:entity.enderman.teleport hostile @a 8.5 42 19.5 0.5 0.4 1
schedule function station9:fx/c1_on 25t
