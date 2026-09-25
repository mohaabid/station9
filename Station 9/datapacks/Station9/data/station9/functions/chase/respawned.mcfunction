# back at the generator; it comes through the door again after a moment
tp @e[tag=s9_hunter] 49.6 41 20.0 -90 0
scoreboard players set #hnode s9 30
scoreboard players set #hnext s9 -1
scoreboard players set #htarget s9 30
scoreboard players set #hwait s9 0
scoreboard players set #hmode s9 5
scoreboard players set #hspd s9 232
scoreboard players set #hgrace s9 100
function station9:ai/to_player
title @a times 10 50 20
title @a subtitle {"text": "It lets you go. For now.", "color": "dark_red"}
title @a title {"text": " ", "color": "dark_red", "bold": true}
