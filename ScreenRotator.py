#!/usr/bin/env python3

# Screen rotator and other useful switches for the tablet mode of Ubuntu/Mint Linux.
# origially from https://github.com/frecel/ScreenRotator
# Yu Heng (henrysting@126.com) modified and tested on Thinkpad X1 Yoga 
# with Linux Mint 19.3 (kernel 5.0.0-32), Cinnamon 64-Bit
# It should also work for other laptops with the Wacom screen and stylus. 
# https://github.com/henrysting/ScreenRotator
#
# Changelog: 
# 2017-11-13: Start
# 2018-02-09: add touchscreen on/off, onboard
# 2018-02-10: add trackpoint on/off, snapshot
# 2020.05.22: update xrandr command for Mint Linux 19.3

import signal
from subprocess import call, check_output
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as AppIndicator

APPINDICATOR_ID = "screenrotator"

pen_id = ""
finger_id = ""
touchpad_id = ""
trackpoint_id = ""
screen_id = ""

try:
    outext = check_output("xsetwacom --list devices | grep stylus | sed 's/.*id//' | awk '{print $2}'", shell=True)
    pen_id = outext.decode('ascii').strip()
except BaseException:
    print("Stylus is not found. Please check the output of xinput.")
        
try:
    outext = check_output("xsetwacom --list devices | grep Finger | sed 's/.*id//' | awk '{print $2}'", shell=True)
    finger_id = outext.decode('ascii').strip()
except BaseException:
    print("Touch Screen is not found. Please check the output of xinput.")
    
try:
    outext = check_output("xinput -list | grep TouchPad | sed 's/.*id=//' | awk '{print $1}'", shell=True)
    touchpad_id = outext.decode('ascii').strip()
except BaseException:
    print("TouchPad is not found. Please check the output of xinput.")
    
try:
    outext = check_output("xrandr | grep ' connected' | awk '{print $1}'", shell=True)
    screen_id = outext.decode('ascii').strip()
except BaseException:
    print("Screen is not found. Please check the output of xrandr.")
    
try:
    outext = check_output("xinput -list | grep TrackPoint | sed 's/.*id=//' | awk '{print $1}'", shell=True)
    trackpoint_id = outext.decode('ascii').strip()
except BaseException:
    print("TrackPoint is not found. Please check the output of xinput.")
    
def main():
    import os        

    root=os.path.dirname(os.path.abspath(__file__))
    print(root)
    indicator = AppIndicator.Indicator.new(APPINDICATOR_ID, root+'/icon.svg', AppIndicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    Gtk.main()
        
def build_menu():
    menu = Gtk.Menu()
       
    #reset
    item_reset = Gtk.MenuItem('Normal')
    item_reset.connect('activate', reset_screen)
    menu.append(item_reset)
    #rotate left
    item_rotate = Gtk.MenuItem('Rotate Left')
    item_rotate.connect('activate', rotate_screen)
    menu.append(item_rotate)
    #flip
    item_flip = Gtk.MenuItem('Flip Vertical')
    item_flip.connect('activate', flip_screen)
    menu.append(item_flip)
    #rotate right
    item_rotate_right = Gtk.MenuItem('Rotate Right')
    item_rotate_right.connect('activate', rotate_screen_right)
    menu.append(item_rotate_right)
    #seperator
    seperator = Gtk.SeparatorMenuItem()
    menu.append(seperator)
        
    ### battery tray contains the brightness control
    #~ #brightness
    #~ item_brightness_up = Gtk.MenuItem('Brightness +')
    #~ item_brightness_up.connect('activate', increase_brightness)
    #~ menu.append(item_brightness_up)
    #~ item_brightness_down = Gtk.MenuItem("Brightness -")
    #~ item_brightness_down.connect('activate', decrease_brightness)
    #~ menu.append(item_brightness_down)
    #~ #seperator
    #~ seperator = Gtk.SeparatorMenuItem()
    #~ menu.append(seperator)
    
    
    # onboard keyboard
    item_onboard = Gtk.MenuItem('Keyboard')
    item_onboard.connect('activate', onboard)
    menu.append(item_onboard)
    item_screenshot = Gtk.MenuItem('Screenshot')
    item_screenshot.connect('activate', screenshot)
    menu.append(item_screenshot)
    #seperator
    seperator = Gtk.SeparatorMenuItem()
    menu.append(seperator)
    
    if finger_id.isdigit():
            
        #touch screen    
        item_touchscreen_off = Gtk.MenuItem('TouchScreen off')
        item_touchscreen_off.connect('activate', touchscreen_off)
        menu.append(item_touchscreen_off)
        item_touchscreen_on = Gtk.MenuItem("TouchScreen on")
        item_touchscreen_on.connect('activate', touchscreen_on)
        menu.append(item_touchscreen_on)
        #seperator
        seperator = Gtk.SeparatorMenuItem()
        menu.append(seperator)
        
    
    if trackpoint_id.isdigit():
            
        #touch pad
        item_trackpoint_off = Gtk.MenuItem('TrackPoint off')
        item_trackpoint_off.connect('activate', trackpoint_off)
        menu.append(item_trackpoint_off)
        item_trackpoint_on = Gtk.MenuItem("TrackPoint on")
        item_trackpoint_on.connect('activate', trackpoint_on)
        menu.append(item_trackpoint_on)
        #seperator
        seperator = Gtk.SeparatorMenuItem()
        menu.append(seperator)
        
    if touchpad_id.isdigit():
            
        #touch pad
        item_touchpad_off = Gtk.MenuItem('TouchPad off')
        item_touchpad_off.connect('activate', touchpad_off)
        menu.append(item_touchpad_off)
        item_touchpad_on = Gtk.MenuItem("TouchPad on")
        item_touchpad_on.connect('activate', touchpad_on)
        menu.append(item_touchpad_on)
        #seperator
        seperator = Gtk.SeparatorMenuItem()
        menu.append(seperator)
    
    #quit
    item_quit = Gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def reset_screen(source):
    #~ call(["xrandr", "-o", "normal"])
    call(["xrandr", "--output", screen_id, "--rotate", "normal"])
    if pen_id.isdigit():
        call(["xsetwacom", "set", pen_id, "rotate","none"])
    if finger_id.isdigit():
        call(["xsetwacom", "set", finger_id, "rotate","none"])
    
def rotate_screen(source):
    #~ call(["xrandr", "-o", "left"])
    call(["xrandr", "--output", screen_id, "--rotate", "left"])
    if pen_id.isdigit():
        call(["xsetwacom", "set", pen_id, "rotate","ccw"])
    if finger_id.isdigit():
        call(["xsetwacom", "set", finger_id, "rotate","ccw"])

def rotate_screen_right(source):
    #~ call(["xrandr", "-o", "right"])
    call(["xrandr", "--output", screen_id, "--rotate", "right"])
    if pen_id.isdigit():
        call(["xsetwacom", "set", pen_id, "rotate","cw"])
    if finger_id.isdigit():
        call(["xsetwacom", "set", finger_id, "rotate","cw"])
    
def flip_screen(source):
    #~ call(["xrandr", "-o", "inverted"])
    call(["xrandr", "--output", screen_id, "--rotate", "inverted"])
    if pen_id.isdigit():
        call(["xsetwacom", "set", pen_id, "rotate","half"])
    if finger_id.isdigit():
        call(["xsetwacom", "set", finger_id, "rotate","half"])

def touchscreen_off(source):
    call(["xinput", "disable", finger_id])

def touchscreen_on(source):
    call(["xinput", "enable", finger_id])


def touchpad_off(source):
    call(["xinput", "disable", touchpad_id])

def touchpad_on(source):
    call(["xinput", "enable", touchpad_id])

    
def trackpoint_off(source):
    call(["xinput", "disable", trackpoint_id])

def trackpoint_on(source):
    call(["xinput", "enable", trackpoint_id])


def onboard(source):
    call(["onboard"])
    
def screenshot(source):
    call(["gnome-screenshot", "-i"])
    
### sudo apt install xbacklight

def increase_brightness(source):
    call(["xbacklight", "-inc", "20"])

def decrease_brightness(source):
    call(["xbacklight", "-dec", "20"])

if __name__ == "__main__":
    #make sure the screen is in normal orientation when the script starts
    #~ call(["xrandr", "-o", "normal"])
    call(["xrandr", "--output ",screen_id," --rotate", "normal"])
    if pen_id.isdigit():
        call(["xsetwacom", "set", pen_id, "rotate","none"])
    if finger_id.isdigit():
        call(["xsetwacom", "set", finger_id, "rotate","none"])
    
    #keyboard interrupt handler
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
