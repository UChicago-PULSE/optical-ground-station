Testing Camera: ZWO ASI 1600MM Pro Cooled Monochrome Astronomy Camera 
Filter Wheel: ZWO 7 Position Filter Wheel

1. for testing purposes, figure out how to control ZWO EFW from a mac
2. find out how to read images from USB into Python (use ZWO manuals)
3. platesolving: send data to ASTAP to retreive image coordinates from starfield 
4. figure out how to send platesolves to Celestron pointing model
5. the tracking itself.

TWO MAIN ROUTINES:
1. the alignment and platesolving to build initial pointing model
2. the tracking sequence loop itself

So we start in acquisition.py, then move to platesolve.py, then to alignment.py. Then we can move on to tracking.py, which calls acquisition in a loop. 

Resources:
- camera manual: https://i.zwoastro.com/zwo-website/manuals/ASI1600_Manual_EN_V1.5.pdf
- ashley camera overview (for background): https://docs.google.com/document/d/17lAU4afn3r8zSEJqAYe9tzgu8W5-umML0QxH84Hy_TY/edit?tab=t.0

- python wrapping: https://github.com/python-zwoasi/python-zwoasi/blob/master/zwoasi/__init__.py
python wrapping documentation: https://zwoasi.readthedocs.io/en/latest/


- NINA source code (camera control): https://bitbucket.org/Isbeorn/nina/src/master/NINA.Equipment/Equipment/MyCamera/ASICamera.cs
- NINA source code (filter wheel): https://bitbucket.org/Isbeorn/nina/src/master/NINA.Equipment/Equipment/MyFilterWheel/ASIFilterWheel.cs

- SDK (software development kit) manual for camera with example code: https://zwoastro.yuque.com/olyczd/sfwyw6/kpde2odaw3h4ekix

Ashley Immediate Goals:
April 6: Answer foundational question questions about camera. How do we communicate with it? Go thru SDK.
April 13: Write code to perform basic tasks. Connect to camera from computer. Take image. Save image.
April 20: Make comprehensive plan with Rodrigo about what the tracking camera needs to accomplish and what tasks it will do.
