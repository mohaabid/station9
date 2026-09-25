execute store result storage station9:ai q.t int 1 run scoreboard players get #tab s9
execute store result storage station9:ai q.a int 1 run scoreboard players get #hnode s9
execute store result storage station9:ai q.b int 1 run scoreboard players get #htarget s9
function station9:ai/route_m with storage station9:ai q
execute if score #hnext s9 = #hnode s9 run scoreboard players set #hnext s9 -1
tag @e[tag=s9_next] remove s9_next
execute as @e[tag=s9_node] if score @s s9_id = #hnext s9 run tag @s add s9_next
