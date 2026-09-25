scoreboard players set #kpwait s9 1
playsound station9:sfx.beep_bad block @a 49 53 23 1 1 0
data modify block 49 53 23 front_text.messages set value ['{"text": "STAIR OVERRIDE"}','{"text": "DENIED"}','{"text": ""}','{"text": ""}']
data modify block 49 53 23 front_text.color set value "red"
schedule function station9:b8/code_reset 30t
