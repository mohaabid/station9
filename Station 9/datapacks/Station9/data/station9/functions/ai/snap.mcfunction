execute at @e[tag=s9_next,limit=1] run tp @e[tag=s9_hunter] ~ ~ ~
scoreboard players operation #hnode s9 = #hnext s9
scoreboard players set #hnext s9 -1
execute if score #hnode s9 = #htarget s9 run return run function station9:ai/arrived
function station9:ai/route
