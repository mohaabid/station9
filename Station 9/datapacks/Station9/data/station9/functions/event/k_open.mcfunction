scoreboard players set #stage s9 4
fill 30 41 21 31 43 21 minecraft:air
playsound minecraft:block.note_block.pling block @a 28 42 20 1 2 1
playsound minecraft:block.iron_door.open block @a 30.5 42 21 1 0.6 1
playsound minecraft:block.piston.contract block @a 30.5 42 21 1 0.6 1
data modify block 28 43 20 front_text.messages set value ['{"text": "ACCESS"}','{"text": "GRANTED"}','""','""']
data modify block 28 43 20 front_text.color set value "lime"
