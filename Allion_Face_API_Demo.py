""" 
Refer from photo_booth program for GUI testing, ottotwei, 20190121
# USAGE
# python photo_booth.py --output takepictures
"""
# import the necessary packages
from __future__ import print_function
from SigninAPI import SigninAPI
from imutils.video import VideoStream
from picamera import PiCamera
import argparse
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output directory to store snapshots")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

# start the app
pba = SigninAPI(vs, args["output"])
pba.root.mainloop()


"""
Mark following simple calculator, ottowei, 2019011602
from tkinter import *

def frame(root, side):   
    w = Frame(root)
    w.pack(side=side, expand=YES, fill=BOTH)
    return w

def button(root, side, text, command=None): 
    w = Button(root, text=text, command=command) 
    w.pack(side=side, expand=YES, fill=BOTH)
    return w

class Calculator(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.option_add('*Font', 'Verdana 12 bold')  
        self.pack(expand=YES, fill=BOTH)
        self.master.title('Simple Calculator')
        self.master.iconname("calc1")

        display = StringVar()  
        Entry(self, relief=SUNKEN, 
        textvariable=display).pack(side=TOP, expand=YES, fill=BOTH)

        for key in ("123", "456", "789", "-0."):  
            keyF = frame(self, TOP)  
            for char in key:  
                button(keyF, LEFT, char, lambda w=display, c=char: w.set(w.get()+ c )) 
                
        opsF = frame(self, TOP)
        for char in "+-*/=":
            if char == '=':
                btn = button(opsF, LEFT, char)
                btn.bind('<ButtonRelease-1>', lambda e, s=self, w=display: s.calc(w), '+')
            else:
                btn = button(opsF, LEFT, char, lambda w=display, s=' %s '%char: w.set(w.get()+s))
                
        clearF = frame(self, BOTTOM)
        button(clearF, LEFT, 'Clr', lambda w=display: w.set(''))

    def calc(self, display):
        try:
            display.set(eval(display.get()))
        except ValueError:
            display.set("ERROR")

if __name__ == '__main__':
    Calculator().mainloop()
"""
