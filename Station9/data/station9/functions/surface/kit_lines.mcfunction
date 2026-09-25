# wait for the opening briefing to finish
execute unless score #s_intro s9 matches 1 run return run schedule function station9:surface/kit_lines 20t
execute if score #talk s9 matches 1.. run return run schedule function station9:surface/kit_lines 20t
function station9:story/kit
