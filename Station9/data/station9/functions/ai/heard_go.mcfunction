execute if score #hmode s9 matches 2 if score #htarget s9 = #pnode s9 run return 0
scoreboard players set #hmode s9 2
scoreboard players set #hspd s9 95
scoreboard players set #hwait s9 0
scoreboard players operation #htarget s9 = #pnode s9
function station9:ai/retarget
execute if score #s_heard s9 matches 0 if score #talk s9 matches ..0 run function station9:story/heard_hint
