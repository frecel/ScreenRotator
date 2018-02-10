# ScreenRotator+
Small applet assembles screen rotator and other useful switches for the tablet mode of Ubuntu/Mint Linux.
It is an enhancement of the project https://github.com/frecel/ScreenRotator, 
modified and tested on Thinkpad X1 Yoga with Linux Mint 18.2 (kernel 4.10.0-38), Cinnamon 64-Bit.
It should work for other laptops with the Wacom screen and pen. 

![image](https://raw.githubusercontent.com/henrysting/ScreenRotator/master/menu.jpg)

ScreenRotator requires python3-gi to work. You can install it by running:
```
sudo apt install python3-gi
```

Screen brightness adjustment rely on xbacklight. You can install it by running
```
sudo apt install xbacklight
```

Switches of Trackpoint or TouchScreen will not be shown if your laptop do not have corresponding devices.

The icon is from Google's Material Desing icon pack (https://materialdesignicons.com/)

Note: The screen rotating function is incompatible  with the kernel 4.13.0-16. 
