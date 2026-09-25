scoreboard players set #kscare s9 1
setblock 31 44 23 minecraft:redstone_lamp[lit=false]
playsound minecraft:block.redstone_torch.burnout block @a 31 44 23 0.3 1.4 1
schedule function station9:event/k_scare_2 6t
