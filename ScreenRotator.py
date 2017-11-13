#!/usr/bin/env python3

# https://github.com/frecel/ScreenRotator
# modified for Thinkpad X1 Yoga at 2017-11-10

import os
import signal
from subprocess import call, check_output
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as AppIndicator

APPINDICATOR_ID = "screenrotator"

pen_id = ""
try:
    outext = check_output("xsetwacom --list devices | grep stylus | sed 's/.*id//' | awk '{print $2}'", shell=True)
    pen_id = outext.decode('ascii').strip()
except BaseException:
    print("Stylus is not found. Please check the output of xinput.")
        
def main():
        
    if pen_id !="":
        indicator = AppIndicator.Indicator.new(APPINDICATOR_ID, './icon.svg', AppIndicator.IndicatorCategory.SYSTEM_SERVICES)
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
    #brightness
    item_brightness_up = Gtk.MenuItem('Brightness -')
    item_brightness_up.connect('activate', increase_brightness)
    menu.append(item_brightness_up)
    item_brightness_down = Gtk.MenuItem("Brightness +")
    item_brightness_down.connect('activate', decrease_brightness)
    menu.append(item_brightness_down)
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
    global pen_id
    call(["xrandr", "-o", "normal"])
    call(["xsetwacom", "set", pen_id, "rotate","none"])
    
def rotate_screen(source):
    global pen_id
    call(["xrandr", "-o", "left"])
    call(["xsetwacom", "set", pen_id, "rotate","ccw"])

def rotate_screen_right(source):
    global pen_id
    call(["xrandr", "-o", "right"])
    call(["xsetwacom", "set", pen_id, "rotate","cw"])
    
def flip_screen(source):
    global pen_id
    call(["xrandr", "-o", "inverted"])
    call(["xsetwacom", "set", pen_id, "rotate","half"])

### sudo apt install xbacklight

def increase_brightness():
    call(["xbacklight", "-inc", "20"])

def decrease_brightness():
    call(["xbacklight", "-dec", "20"])

if __name__ == "__main__":
    #make sure the screen is in normal orientation when the script starts
    call(["xrandr", "-o", "normal"])
    #keyboard interrupt handler
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
