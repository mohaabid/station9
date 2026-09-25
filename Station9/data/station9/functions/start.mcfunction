# Rebuild everything and play from the top
title @a times 0 200 20
title @a title {"text": " "}
title @a subtitle {"text": "rebuilding the station...", "color": "dark_gray"}
effect give @a minecraft:blindness 30 0 true
gamemode spectator @a
function station9:reset
function station9:build/surface_terrain
schedule function station9:build/surface_compound 4t
schedule function station9:build/shells 6t
schedule function station9:build/rooms_walls 8t
schedule function station9:build/rooms_air 10t
schedule function station9:build/wear 12t
schedule function station9:build/openings 14t
schedule function station9:build/details9 16t
schedule function station9:build/details8 18t
schedule function station9:build/emergency_off 20t
schedule function station9:build/lamps_off 22t
schedule function station9:start2 26t
