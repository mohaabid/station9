# it gives up on the locker and goes back the way it came; the chase resumes when you move
scoreboard players set #hmode s9 2
scoreboard players set #hspd s9 95
scoreboard players set #htarget s9 7
function station9:ai/retarget
schedule function station9:chase/resume 140t
