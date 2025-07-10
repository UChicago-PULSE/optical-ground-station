### Welcome to the Tracking Camera code!
This code was written by Ashley Ashiku (telescope engineer) but utilizes Python wrappers (written by Steve Marple 2017, search python-zwoasi) around C commands for ZWO ASI cameras from the software development kit.

This code controls and interfaces with the PULSE-A tracking camera, which is an integral part of our optical ground station's ability to track our Payload beacon. 

There are several files associated with this, which I have commented out step-by-step. 
The path is as follows:

#### 1. Installation Instructions
Before you look at a single line of code, there is a number of installations you need to make first on your laptop. This is the hardest part-- I promise it's all smooth sailing from here! You'll need to 
install the software development kit (SDK) code and libusb, which allows you to connect to the camera through USB. Think of it as the dictionary (SDK) and translator app (libusb) that you need to communicate
with the camera!

##### Download the SDK code [here at the ZWO website](https://www.zwoastro.com/software/).
At the top of the screen, navigate to Others >> For Developers and download the "ASI Camera SDK". Put this in your PULSE-A folder or whatever you're using-- you'll need this later!

##### Download libusb
This is the tricky part. Download libusb using homebrew. Note-- for Macbooks, the package and its dependencies only work with Intel Macs, not Apple Silicon Macs. My Silicon users, do not fear, I am one too!
Luckily, I went through the maze already so you don't have to. Go into your Terminal, create a new duplicate terminal, go to "Get Info", and check "Open using Rosetta". This makes your terminal emulate an Intel Mac. 
You need the x86_64 version, NOT arm64. Run "uname -m" in your terminal to check. 

Then, install libusb: "brew install libusb".

#### 2. cameraconnect.py
Now, you're onto the code! The next step is to connect to the camera. We connect through a USB directly into your laptop. Find any connectors/converters you need for this step!

Heads up: you might see "WARNING:root:ASI SDK library not found" when you first run this code. Ignore it. 

This code is very straightforward. Follow the comments.

#### 3. camerapicture.py
Now, it's time to start taking images! This file contains 2 helper functions and one function to take an eight bit mono image with any gain and exposure time you like.
In all honesty, I don't remember what the cam_1 = camconnect() is from at the moment and I can't test it without the camera! Will add more later...
