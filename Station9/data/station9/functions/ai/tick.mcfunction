execute unless entity @e[tag=s9_hunter] run return 0
scoreboard players add #e s9 1
scoreboard players operation #e5 s9 = #e s9
scoreboard players operation #e5 s9 %= #5 s9
execute if score #e5 s9 matches 0 as @a[limit=1] at @s as @e[tag=s9_node,sort=nearest,limit=1] run scoreboard players operation #pnode s9 = @s s9_id
function station9:ai/sense
function station9:ai/think
execute if score #hmode s9 matches 4 if score #lkphase s9 matches 1 if score #frozen s9 matches 0 run function station9:ai/lk_approach
execute if score #hwait s9 matches 1 run function station9:ai/after
execute if score #hwait s9 matches 1.. run scoreboard players remove #hwait s9 1
execute if score #frozen s9 matches 0 if score #hwait s9 matches 0 if score #hnext s9 matches 0.. if score #hgrace s9 matches ..0 run function station9:ai/step
execute if score #frozen s9 matches 0 if score #hwait s9 matches 0 if score #hnext s9 matches ..-1 if score #hgrace s9 matches ..0 if score #hmode s9 matches 3..5 unless score #hmode s9 matches 4 run function station9:ai/approach
execute if score #hgrace s9 matches 1.. run scoreboard players remove #hgrace s9 1
function station9:ai/catchcheck
function station9:ai/presence
