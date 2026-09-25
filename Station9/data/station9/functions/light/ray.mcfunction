scoreboard players add #ls s9 1
# stop at the creature so it stands in the beam
execute positioned ~ ~-1.6 ~ if entity @e[tag=s9_hunter,distance=..1.1] run scoreboard players set #beam s9 1
execute if score #beam s9 matches 1 run return run function station9:light/place
execute unless block ^ ^ ^0.5 #station9:beam_through run return run function station9:light/place
execute if score #ls s9 matches 22.. run return run function station9:light/place
execute positioned ^ ^ ^0.5 run function station9:light/ray
