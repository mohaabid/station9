setblock 36 101 27 minecraft:spruce_button[face=wall,facing=west,powered=false]
execute if score #signed s9 matches 1 run return 0
scoreboard players set #signed s9 1
data modify block 36 102 27 front_text.messages set value ['{"text": "CONTRACTOR B9"}','{"text": "01:12  -"}','{"text": ""}','{"text": ""}']
data modify block 36 102 27 front_text.color set value "blue"
playsound minecraft:item.book.page_turn block @a 36 101 27 1 1 0
schedule function station9:surface/signed 20t
