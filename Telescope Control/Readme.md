This folder holds the code to control the telescope. 
  -Nexstar.py outline sthe serial commands to control the telescope and should be imported to use those commands
  -OGS_control_call.py contains a schedule_gen class and a OGS controll class. The schedule_gen class takes in a position as a function fo time 
  and creates a schedule of commands, OGS_control has commands to actually slew the telescope and follow the schedule created by schedule_gen
  - Slew rate calculations contains the calculations to obtain the slew rates necessary to track the satellite, goal is to create a function
  that has as its only input being time and can be fed into schedule_gen. 
