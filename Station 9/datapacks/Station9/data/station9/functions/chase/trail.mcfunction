# breadcrumbs: if it falls too far behind, it reappears where you were 3 seconds ago
execute at @a run summon minecraft:marker ~ ~ ~ {Tags:["s9","s9_trail"]}
scoreboard players add @e[tag=s9_trail] s9_age 1
kill @e[tag=s9_trail,scores={s9_age=13..}]
execute as @e[tag=s9_hunter] at @s unless entity @a[distance=..16] run tp @s @e[tag=s9_trail,scores={s9_age=6},limit=1]
