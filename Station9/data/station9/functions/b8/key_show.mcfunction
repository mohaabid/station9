execute if score #digits s9 matches 0 run data modify block 49 53 23 front_text.messages set value ['{"text": "STAIR OVERRIDE"}','{"text": "_ _ _ _"}','{"text": ""}','{"text": ""}']
execute if score #digits s9 matches 1 run data modify block 49 53 23 front_text.messages set value ['{"text": "STAIR OVERRIDE"}','{"text": "* _ _ _"}','{"text": ""}','{"text": ""}']
execute if score #digits s9 matches 2 run data modify block 49 53 23 front_text.messages set value ['{"text": "STAIR OVERRIDE"}','{"text": "* * _ _"}','{"text": ""}','{"text": ""}']
execute if score #digits s9 matches 3 run data modify block 49 53 23 front_text.messages set value ['{"text": "STAIR OVERRIDE"}','{"text": "* * * _"}','{"text": ""}','{"text": ""}']
execute if score #digits s9 matches 4 run data modify block 49 53 23 front_text.messages set value ['{"text": "STAIR OVERRIDE"}','{"text": "* * * *"}','{"text": ""}','{"text": ""}']
execute if score #digits s9 matches 4 if score #code s9 matches 214 run return run function station9:b8/code_ok
execute if score #digits s9 matches 4 run function station9:b8/code_bad
