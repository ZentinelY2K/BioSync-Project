"""
Experiment:
The laptop - being the hub for the hotspot - and my laptop - the sender - where place across different places
relative to the robot, a stopwatch and measuring tape were used to measure time and distance.
"""
#10 centimeters = 0
#20 centimeters = 0
#Skipped to infront of my house with the robot standing by the door across the street at roughly 10800 cm = 0.10-0,  could've been
#my own delay at stopping the stopwatch
#laundry room (1 closed door,2 curves,1400) time = 0.72
#upstairs (no doors,no curves,1000,roughly 215 altitude) time = 1.08
#my room upstaris (1 do or, 1 curve, 1400, roughly 215 altitude) time = 1.59
#upstairs couch (no doors, 1 curve, 2000, 215 altitiude) time = 0.75
#upstairs parents room (1 door, 2 curves, 2400, 215 altitude) time =  1.89
#upstairs parents room bathroom (2 doors, 5 curves, 2800, 215 altitude) time = 3.68
#results:
"""
It was determined that altitude and mass heavily affect the robot's reaction time, having observed that 
when positioning myself on a linear distance it would give insignificant results that could be interpreted as instant reaction
time, whereas if i went upstairs or locked myself in rooms the results would be clear.
A great example of this is the upstairs couch, even though it has more distance from the robot than my room it had no doors
and therefore there was less mass blocking the signal so it reacted faster.
This makes sense because wireless earbuds and other devices work the same way, the mass of the walls heavily affect the
delay of them or causes errors.

Why this matters: In a Human-Machine interface is important to have quick, reliable systems that can react to threats. For 
instance a bomb disposal robot needs to quickly take action and humans need to be far from the zone due to danger, wireless
effectiveness is an area of improvement.
"""