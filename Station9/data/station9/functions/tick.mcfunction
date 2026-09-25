execute as @a[tag=!s9_seen] run function station9:join
execute if score #stage s9 matches 2..6 run scoreboard players add #time s9 1
execute if score #stage s9 matches 1..5 run function station9:tick/flicker
execute if score #stage s9 matches 2..5 run function station9:tick/explore
execute if score #stage s9 matches 6 run function station9:tick/chase
