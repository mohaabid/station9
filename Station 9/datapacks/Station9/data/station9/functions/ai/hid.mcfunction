# you got into a locker
execute if score #hmode s9 matches 3 if score #seenago s9 matches ..40 run return run function station9:ai/check_locker
execute if score #hmode s9 matches 5 if score #seenago s9 matches ..40 run return run function station9:ai/check_locker
execute if score #hmode s9 matches 3 run return run function station9:ai/lost_you
execute if score #hmode s9 matches 5 run return run function station9:ai/lost_you
