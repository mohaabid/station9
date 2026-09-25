# a noise: go and look
execute if score #hmode s9 matches 4..6 run return 0
execute if score #hgrace s9 matches 1.. run return 0
execute if score #hmode s9 matches 1..2 run function station9:ai/heard_go
execute if score #hmode s9 matches 3 run scoreboard players set #lost s9 0
execute if score #hmode s9 matches 3 run function station9:ai/to_player
