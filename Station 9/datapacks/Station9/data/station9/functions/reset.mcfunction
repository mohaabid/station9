# Put the whole station back to its starting state
kill @e[tag=s9]
function station9:rules
stopsound @a
effect clear @a
clear @a
scoreboard players reset * s9_hud
scoreboard players set #stage s9 0
scoreboard players set #time s9 0
scoreboard players set #deaths s9 0
scoreboard players set #light s9 0
scoreboard players set #charge s9 0
scoreboard players set #fried s9 0
scoreboard players set #talk s9 0
scoreboard players set #amb s9 0
scoreboard players set #area s9 0
scoreboard players set #hudt s9 0
scoreboard players set #tapes s9 0
scoreboard players set #t_hale1 s9 0
scoreboard players set #t_hale2 s9 0
scoreboard players set #t_marsh s9 0
scoreboard players set #marsh s9 0
scoreboard players set #ending s9 0
scoreboard players set #signed s9 0
scoreboard players set #kit s9 0
scoreboard players set #cam s9 0
scoreboard players set #hmode s9 0
scoreboard players set #hnode s9 0
scoreboard players set #hnext s9 0
scoreboard players set #htarget s9 0
scoreboard players set #hspd s9 0
scoreboard players set #hwait s9 0
scoreboard players set #tab s9 0
scoreboard players set #hgrace s9 0
scoreboard players set #hdist s9 0
scoreboard players set #hstride s9 0
scoreboard players set #watched s9 0
scoreboard players set #wtime s9 0
scoreboard players set #frozen s9 0
scoreboard players set #los s9 0
scoreboard players set #beam s9 0
scoreboard players set #pnode s9 0
scoreboard players set #lost s9 0
scoreboard players set #stingcd s9 0
scoreboard players set #catching s9 0
scoreboard players set #hidden s9 0
scoreboard players set #code s9 0
scoreboard players set #digits s9 0
scoreboard players set #e s9 0
scoreboard players set #seenago s9 0
scoreboard players set #lkphase s9 0
scoreboard players set #s_intro s9 0
scoreboard players set #s_walk s9 0
scoreboard players set #s_hut s9 0
scoreboard players set #s_coffee s9 0
scoreboard players set #s_incage s9 0
scoreboard players set #inhut s9 0
scoreboard players set #s_called s9 0
scoreboard players set #s_relay s9 0
scoreboard players set #s_doorA s9 0
scoreboard players set #s_bed s9 0
scoreboard players set #s_knock s9 0
scoreboard players set #s_ring s9 0
scoreboard players set #s_window s9 0
scoreboard players set #s_ceiling s9 0
scoreboard players set #s_turn s9 0
scoreboard players set #s_turn2 s9 0
scoreboard players set #s_st3 s9 0
scoreboard players set #hint s9 0
scoreboard players set #inA s9 0
scoreboard players set #window s9 0
scoreboard players set #wlook s9 0
scoreboard players set #s_release s9 0
scoreboard players set #kpwait s9 0
scoreboard players set #s_code s9 0
scoreboard players set #rings s9 0
scoreboard players set #s_answered s9 0
scoreboard players set #teach s9 0
scoreboard players set #tw s9 0
scoreboard players set #tt s9 0
scoreboard players set #tu s9 0
scoreboard players set #s_nofuse s9 0
scoreboard players set #s_marsh s9 0
scoreboard players set #s_wh1 s9 0
scoreboard players set #s_wh2 s9 0
scoreboard players set #mirror s9 0
scoreboard players set #cscene s9 0
scoreboard players set #b9t s9 0
scoreboard players set #s_watch s9 0
scoreboard players set #s_deny s9 0
scoreboard players set #tapeon s9 0
scoreboard players set #s_b8chase s9 0
scoreboard players set #s_collapse s9 0
scoreboard players set #siren s9 0
scoreboard players set #ride s9 0
scoreboard players set #dark s9 0
scoreboard players set #s_walked s9 0
scoreboard players set #s_heard s9 0
scoreboard players set #s_caught s9 0
scoreboard players set #hnext s9 -1
scoreboard players set #charge s9 3600
scoreboard players set @a s9_deaths 0
scoreboard players set @a s9_click 0
tag @a remove s9_hidden
setworldspawn 69 101 18
spawnpoint @a 69 101 18
effect give @a minecraft:saturation infinite 0 true
data remove storage station9:ai m
schedule clear station9:ai/catch2
schedule clear station9:ai/locker_breath
schedule clear station9:b8/code_reset
schedule clear station9:b8/gate_jammed
schedule clear station9:b8/relay_lights
schedule clear station9:b8/ring
schedule clear station9:b8/window_lamp
schedule clear station9:b8/window_line
schedule clear station9:b9/fuse_lights
schedule clear station9:b9/fuse_line
schedule clear station9:b9/office_slam
schedule clear station9:chase/resume
schedule clear station9:end/a_black
schedule clear station9:end/a_scare
schedule clear station9:end/a_scare2
schedule clear station9:end/a_seq/00
schedule clear station9:end/a_seq/01
schedule clear station9:end/a_seq/02
schedule clear station9:end/a_seq/03
schedule clear station9:end/a_seq/04
schedule clear station9:end/a_seq/05
schedule clear station9:end/a_seq/06
schedule clear station9:end/b_down
schedule clear station9:end/b_line
schedule clear station9:end/b_seq/00
schedule clear station9:end/b_seq/01
schedule clear station9:end/b_seq/02
schedule clear station9:end/b_seq/03
schedule clear station9:end/b_seq/04
schedule clear station9:end/b_seq/05
schedule clear station9:end/b_seq/06
schedule clear station9:end/b_seq/07
schedule clear station9:end/b_title
schedule clear station9:end/gate_up
schedule clear station9:end/stats
schedule clear station9:fx/on_c2t
schedule clear station9:fx/on_c3t
schedule clear station9:fx/on_c3u
schedule clear station9:fx/on_c4t
schedule clear station9:fx/on_c4u
schedule clear station9:fx/on_c4v
schedule clear station9:fx/on_e8a
schedule clear station9:fx/on_e8b
schedule clear station9:fx/on_e8c
schedule clear station9:fx/on_e8d
schedule clear station9:fx/on_o1
schedule clear station9:fx/on_w1
schedule clear station9:fx/shake
schedule clear station9:fx/storm
schedule clear station9:gen/sequence/00
schedule clear station9:gen/sequence/01
schedule clear station9:gen/sequence/02
schedule clear station9:gen/sequence/03
schedule clear station9:gen/sequence/04
schedule clear station9:line/a1_hint1
schedule clear station9:line/a1_hint2
schedule clear station9:line/a1_stairs
schedule clear station9:line/a1_window
schedule clear station9:line/a2_caught
schedule clear station9:line/a2_heard
schedule clear station9:line/a2_lockers
schedule clear station9:line/a2_marsh
schedule clear station9:line/a2_nofuse
schedule clear station9:line/wh_hear
schedule clear station9:line/wh_off
schedule clear station9:start
schedule clear station9:story/arrive/00
schedule clear station9:story/arrive/01
schedule clear station9:story/arrive/02
schedule clear station9:story/caught_line
schedule clear station9:story/ceiling/01
schedule clear station9:story/ceiling/02
schedule clear station9:story/ceiling/03
schedule clear station9:story/ceiling/04
schedule clear station9:story/ceiling/05
schedule clear station9:story/descend
schedule clear station9:story/kit/00
schedule clear station9:story/kit/01
schedule clear station9:story/kit/02
schedule clear station9:story/lift_arrives/00
schedule clear station9:story/lift_arrives/01
schedule clear station9:story/lift_arrives/02
schedule clear station9:story/lift_arrives/03
schedule clear station9:story/lockdown/00
schedule clear station9:story/lockdown/01
schedule clear station9:story/lockdown/02
schedule clear station9:story/lockers_line
schedule clear station9:story/opening/01
schedule clear station9:story/opening/02
schedule clear station9:story/opening/03
schedule clear station9:story/opening/04
schedule clear station9:story/opening/05
schedule clear station9:story/phone/00
schedule clear station9:story/phone/01
schedule clear station9:story/phone/02
schedule clear station9:story/phone/03
schedule clear station9:story/relay/00
schedule clear station9:story/relay/01
schedule clear station9:story/relay/02
schedule clear station9:story/relay/03
schedule clear station9:story/relay/04
schedule clear station9:story/ride/02
schedule clear station9:story/ride/03
schedule clear station9:story/ride/04
schedule clear station9:story/ride/05
schedule clear station9:story/ride/06
schedule clear station9:story/ride/07
schedule clear station9:story/ride/08
schedule clear station9:story/ride/09
schedule clear station9:story/ride/10
schedule clear station9:story/ride/11
schedule clear station9:story/ride/12
schedule clear station9:story/ride/13
schedule clear station9:story/ride/14
schedule clear station9:story/ride/15
schedule clear station9:story/ride/16
schedule clear station9:story/ride/17
schedule clear station9:story/ride/18
schedule clear station9:story/ride/19
schedule clear station9:story/ride/20
schedule clear station9:story/ride/21
schedule clear station9:story/ride/22
schedule clear station9:story/ride/23
schedule clear station9:story/ride/24
schedule clear station9:story/ride/25
schedule clear station9:story/ride/26
schedule clear station9:story/rule/00
schedule clear station9:story/rule/01
schedule clear station9:story/stairs_down/00
schedule clear station9:story/stairs_down/01
schedule clear station9:story/up/00
schedule clear station9:story/up/01
schedule clear station9:story/up/02
schedule clear station9:story/up/03
schedule clear station9:story/up/04
schedule clear station9:story/up/05
schedule clear station9:story/up/06
schedule clear station9:story/up/07
schedule clear station9:story/up/08
schedule clear station9:story/up/09
schedule clear station9:story/up/10
schedule clear station9:story/up/11
schedule clear station9:story/up/12
schedule clear station9:story/up/13
schedule clear station9:story/up/14
schedule clear station9:surface/kit_lines
schedule clear station9:surface/signed
