This folder holds the code to control the telescope. 

  - Nexstar.py outlines the serial commands to control the telescope and should be imported to use those commands
  
  - OGS_control_call.py contains a schedule_gen class and a OGS controll class. The schedule_gen class takes in a position as a function fo time 
  and creates a schedule of commands, OGS_control has commands to actually slew the telescope and follow the schedule created by schedule_gen
  
  - Slew rate calculations contains the calculations to obtain the slew rates necessary to track the satellite, goal is to create a function
  that has as its only input being time and can be fed into schedule_gen.

  - From March 2nd 2025, the tracking methods are tested by the RMS of the measured path vs the intended path. The recods jupyter notebook keeps       track of how well tracking methods are matching intended paths.
