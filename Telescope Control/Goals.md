These are the goals for telescope control for the Spring of the 2024-2025 school year:
  - (1)Tracking ISS: The main goal is to at the very least be ready to track the ISS with the tracking camera by the end of the quarter. 
    - (1.1) Create software that takes sat GPS data and outputs schedule for tracking software.
    - (1.2) Integrate the tracking camera
    - (1.3) Telescope pointing calibration (in prog)
    
Now, for sub-goals for each of these larger goals for the quarter:

(1.1):
  - Use software recommended by seth to generate path for satellite given a two line element (TLE). Then use astropy to turn this into AZM and ALT for different times, then use this to output a schedule. 

(1.3): 
  - Address error that happens when slew rate gets to large and everything breaks. 
  - Use simulated sat passes to measure RMS and find an optimal correction factor. This is important to do on top of sin wave tests becasue the real passes could have structure that causes different behavior than we see in sin curves. 
