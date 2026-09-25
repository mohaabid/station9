execute if score #stingcd s9 matches 1.. run scoreboard players remove #stingcd s9 1
execute if score #sees s9 matches 1 if score #hmode s9 matches 1..2 run function station9:ai/spotted
execute if score #hmode s9 matches 3 run function station9:ai/hunt
execute if score #hmode s9 matches 5 run function station9:ai/chase
