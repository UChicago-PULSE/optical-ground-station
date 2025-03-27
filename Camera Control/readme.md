Documentation for the camera code 
https://i.zwoastro.com/zwo-website/manuals/ASI1600_Manual_EN_V1.5.pdf

Testing Camera: ZWO ASI 1600MM Pro Cooled Monochrome Astronomy Camera 
Filter Wheeel: ZWO 7 Position Filter Wheel

1. for testing purposes, figure out how to control ZWO EFW from a mac
2. find out how to read images from USB into Python (use ZWO manuals)
3. platesolving: send data to ASTAP to retreive image coordinates from starfield 
4. figure out how to send platesolves to Celestron pointing model
5. the tracking itself.

TWO MAIN ROUTINES:
1. the alignment and platesolving to build initial pointing model
2. the tracking sequence loop itself
