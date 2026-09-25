title @a actionbar {"text": "ACCESS DENIED - LEVEL 3 KEYCARD REQUIRED", "color": "red"}
playsound minecraft:block.note_block.bass block @a 28 42 20 1 0.5 1
execute if score #kdeny s9 matches 0 run function station9:event/k_deny_hint
