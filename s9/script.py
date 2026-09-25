"""Every spoken line in the map.

Shared by tools/make_audio.py (which voices them) and generate.py (which shows the
subtitles and times the scenes from assets/sounds/manifest.json). `say` is what the
voice reads when it differs from the subtitle (numbers, level names).
"""

SPEAKERS = {
    #          subtitle label,   colour,       voice model,                            processing
    "ops":    ("Reyes",          "dark_aqua",  "en_US-lessac-high",                    "radio"),
    "garble": ("Reyes",          "dark_aqua",  "en_US-lessac-high",                    "garble"),
    "pa":     ("Station PA",     "gold",       "en_GB-cori-high",                      "pa"),
    "hale":   ("Dr. Hale",       "green",      "en_GB-alan-medium",                    "tape"),
    "marsh":  ("M. Marsh",       "green",      "en_US-ryan-high",                      "tape_shaky"),
    "phone":  ("Reyes?",         "dark_aqua",  "en_US-lessac-high",                    "phone"),
    "whisper": ("",              "dark_gray",  "en_US-hfc_male-medium",                "whisper"),
}

L = {}


def line(key, who, text, say=None, speed=1.0):
    L[key] = dict(who=who, text=text, say=say or text, speed=speed)


# --- Act 0: the surface ---------------------------------------------------------
line("a0_arrive", "ops", "Reyes here, radio check. ...Good, I've got you. Sorry about the weather. Welcome to Site 9.",
     "Ray-ess here. Radio check. ... Good, I've got you. Sorry about the weather. Welcome to Site Nine.")
line("a0_gate", "ops", "The gate's been open since the evacuation. Head for the security hut, sign in, then grab the contractor kit from the locker.")
line("a0_walk", "ops", "Nobody's been on site for 41 days. The guard walked off the job the night it went dark. Can't say I blame him.",
     "Nobody's been on site for forty one days. The guard walked off the job the night it went dark. Can't say I blame him.")
line("a0_hut", "ops", "That's the hut. Sign the sheet by the door. Company rules, even now.")
line("a0_signed", "ops", "Thanks. ...Huh. Marsh never signed out. None of the B9 shift did.",
     "Thanks. ... Huh. Marsh never signed out. None of the bee nine shift did.")
line("a0_kit", "ops", "Got the kit? Right-click the flashlight to switch it on. Batteries don't last long down there, so grab any spares you find.",
     "Got the kit? Right click the flashlight to switch it on. Batteries don't last long down there, so grab any spares you find.")
line("a0_coffee", "ops", "Is Frank's coffee machine still in there? Worst coffee on the mountain. Don't drink it. Six weeks.")
line("a0_to_lift", "ops", "The lift house is at the north end, under the headframe. Call the cage.")
line("a0_called", "ops", "It's coming up. The lift still runs on the backup line, so that's something.")
line("a0_in_cage", "ops", "Press B9 when you're ready. I'll talk you down.", "Press bee nine when you're ready. I'll talk you down.")
line("a0_ride1", "ops", "Here's the job. Generator B, bottom level. It failed 41 days ago and took the whole station with it.",
     "Here's the job. Generator B, bottom level. It failed forty one days ago, and took the whole station with it.")
line("a0_ride2", "ops", "Get it running and every light in the place comes back on. The recovery team goes down in the morning. In and out.")
line("a0_ride3", "ops", "What was that? ...Your cage camera just cut out. Probably debris on the roof. Stay still.",
     "What was that? ... Your cage camera just cut out. Probably debris on the roof. Stay still.", speed=0.95)
line("a0_ride4", "ops", "Talk to me. ...Okay. Nearly there. B6. B7...", "Talk to me. ... Okay. Nearly there. bee six. bee seven.")

# --- Act 1: B8 ----------------------------------------------------------------------
line("a1_static", "garble", "...can you hear... cage brakes... B8... don't...", "Can you hear me? The cage brakes locked. You're on bee eight. Don't move.")
line("a1_relay", "pa", "Communications relay online. Backup power at eight percent.", speed=1.1)
line("a1_contact", "ops", "There you are! I lost you for four minutes. The cage brakes locked at B8. Are you hurt? ...Okay. Okay.",
     "There you are! I lost you for four minutes. The cage brakes locked at bee eight. Are you hurt? ... Okay. Okay.")
line("a1_contact2", "ops", "The cage won't move until main power's back, so we do this the hard way. Take the stairs down to B9.",
     "The cage won't move until main power's back, so we do this the hard way. Take the stairs down to bee nine.")
line("a1_locked", "ops", "The stairwell's in lockdown. There's an override panel in the security office, east end of the hall. It needs the duty code.")
line("a1_hint1", "ops", "Security on that shift used times for their codes. The time something happened. Hale's lab logs might have it.")
line("a1_hint2", "ops", "I dug it out of an old maintenance ticket. Try zero, two, one, four.")
line("a1_code_ok", "ops", "That's it, the stairwell's open. Go down to B9.", "That's it. The stairwell's open. Go down to bee nine.")
line("a1_phone_after", "ops", "Who were you talking to? ...The station phones have been dead for six weeks.",
     "Who were you talking to? ... The station phones have been dead for six weeks.")
line("a1_window", "ops", "Your heart rate just spiked. What did you see? ...Okay. Keep going.",
     "Your heart rate just spiked. What did you see? ... Okay. Keep going.")
line("a1_stairs", "ops", "Every level between you and B9 is dark on my board. Keep going down.",
     "Every level between you and bee nine is dark on my board. Keep going down.")
line("phone", "phone", "Hey. It's Reyes. I'm down here with you. I'm in the kitchen, behind the door. ...Come and see.",
     "Hey. It's Ray-ess. I'm down here with you. I'm in the kitchen. Behind the door. ... Come and see.", speed=1.25)

# --- Tapes ------------------------------------------------------------------------------
line("tape_hale1", "hale", "Hale. Day 115, 02:14. The power dipped for less than a second. When the lights came back, Subject 9 was "
     "pressed against the glass. It had been at the back wall. It only moves in the dark.",
     "Hale. Day one fifteen. Oh two fourteen. The power dipped for less than a second. When the lights came back, "
     "Subject Nine was pressed against the glass. It had been at the back wall. It only moves in the dark.", speed=1.05)
line("tape_hale2", "hale", "Hale. Day 121. Marsh is gone. His keycard was on my desk this morning. I didn't put it there. ...It isn't "
     "afraid of the light. It just can't see in the dark. So it listens.",
     "Hale. Day one twenty one. Marsh is gone. His keycard was on my desk this morning. I didn't put it there. ... "
     "It isn't afraid of the light. It just can't see in the dark. So it listens.", speed=1.05)
line("tape_marsh", "marsh", "This is Marsh. If you can hear this, don't start the generator. It turns every light on at once, and then it "
     "sees everything. ...If you have to, and you make it to the lift, kill the cage light before you go up. It rides on the "
     "roof. It can't find you in the dark.",
     "This is Marsh. If you can hear this, don't start the generator. It turns every light on at once, and then it sees "
     "everything. ... If you have to, and you make it to the lift, kill the cage light before you go up. It rides on the roof. "
     "It can't find you in the dark.", speed=1.08)

# --- Act 2: B9 --------------------------------------------------------------------------
line("a2_arrive", "ops", "B9. The generator room is at the east end of the main corridor. ...Wait. Your camera. There's someone at the "
     "end of the corridor.", "bee nine. The generator room is at the east end of the main corridor. ... Wait. Your camera. "
     "There's someone at the end of the corridor.")
line("a2_watch", "ops", "Don't take your eyes off it.", speed=1.1)
line("a2_gone", "ops", "Where did it go? It was right there. ...Keep your light on. Keep moving.",
     "Where did it go? It was right there. ... Keep your light on. Keep moving.")
line("a2_rule", "ops", "Every time your light is on it, it stops. The second it's dark, it moves. Keep it in the light.")
line("a2_heard", "ops", "It heard you. Walk. Don't run.", speed=1.05)
line("a2_lockers", "ops", "Staff lockers. If it comes for you, get inside and shut the door. Don't make a sound.")
line("a2_nofuse", "ops", "Generator B is missing its fuse. There are spares in containment, but that door needs a level 3 keycard.",
     "Generator B is missing its fuse. There are spares in containment, but that door needs a level three keycard.")
line("a2_deny", "ops", "Level 3. Marsh had level 3. Try the staff office, north side of the corridor.",
     "Level three. Marsh had level three. Try the staff office, north side of the corridor.")
line("a2_key", "ops", "That's Marsh's keycard. ...He never signed out.", "That's Marsh's keycard. ... He never signed out.")
line("a2_contain", "ops", "The fuses are in the cell. ...It's in there. Standing in the corner. Keep your light on it and take the fuse.",
     "The fuses are in the cell. ... It's in there. Standing in the corner. Keep your light on it, and take the fuse.")
line("a2_fuse", "ops", "You've got it. Get out of there. Go!", speed=0.9)
line("a2_after_fuse", "ops", "It's gone. ...It's heading east. It knows where you're going.",
     "It's gone. ... It's heading east. It knows where you're going.")
line("a2_caught", "ops", "...You're back. I thought I'd lost you. Stay out of its reach.",
     "You're back. I thought I'd lost you. Stay out of its reach.")
line("a2_marsh", "ops", "Oh, God. That's Marsh. ...I'm sorry. Take his recorder.", "Oh God. That's Marsh. ... I'm sorry. Take his recorder.")

# --- Act 3: the generator and the escape ------------------------------------------------
line("a3_power", "ops", "Power's up! Every level is lighting up on my board!", speed=0.92)
line("a3_wait", "ops", "Wait. Containment B9 reads open. It's read open for 41 days.",
     "Wait. Containment bee nine reads open. It's read open for forty one days.")
line("a3_lockdown", "pa", "Containment breach on level B9. Lockdown in effect.", "Containment breach on level bee nine. Lockdown in effect.")
line("a3_run", "ops", "It's at the door! Maintenance tunnel, south side! Up the service stairs to B8, then the lift! Run!",
     "It's at the door! Maintenance tunnel, south side! Up the service stairs to bee eight, then the lift! Run!", speed=0.85)
line("a3_b8", "ops", "The cage has power now! Get to the lift!", speed=0.88)
line("a3_collapse", "ops", "The hall's coming down! Through the cafeteria!", speed=0.85)
line("a3_lift", "ops", "I've got you! Bringing you up now!", speed=0.9)

# --- Endings ---------------------------------------------------------------------------------
line("e_ride", "ops", "B7. B6. ...You did it. I'm so sorry. Nobody told me what was down there.",
     "bee seven. bee six. ... You did it. I'm so sorry. Nobody told me what was down there.")
line("e_heavy", "ops", "Hang on. Your cage weight reads wrong. It's about two hundred and forty kilos too heavy.")
line("e_dark", "ops", "Why did your light go out? ...Oh. Oh God. It's on the roof. Don't move. Don't make a sound.",
     "Why did your light go out? ... Oh. Oh God. It's on the roof. Don't move. Don't make a sound.")
line("e_out", "ops", "You're at the top. Walk away from the cage. Slowly. I'm sending it back down.")

# --- Whispers (heard once each, never on a loop) -----------------------------------------------
line("wh_off", "whisper", "turn it off", speed=1.3)
line("wh_hear", "whisper", "i can hear you", speed=1.3)
line("wh_stay", "whisper", "stay down here", speed=1.3)
