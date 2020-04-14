from tkinter import *
import tkinter as tk
from tkinter import messagebox
#import board
#import busio
#import adafruit_vl53l0x
import PiMotor
import time
import RPi.GPIO as GPIO

class Window:

    def __init__(self, master):

        #size of user interface
        root.geometry("600x600")
        root.title("Automated iButton Device GUI")

        #creating the buttons, the command atribute calls the function
        self.start_button = Button(master, text="Start System", height=2, width=12, bd=3, command=self.start)
        self.test_button = Button(master, text="Test Component", height=2, width=12, bd=3, command=self.test)
        self.report_button = Button(master, text="View Report", height=2, width=12, bd=3)
        self.stop_button = Button(master, text="Stop", height=2, width=12, bd=3)

        #displaying the buttons in the GUI, change relx and rely to move buttons around
        self.start_button.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.test_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.report_button.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.stop_button.place(relx=0.5, rely=0.9, anchor=CENTER)

    #this function will handle the starting process of the device
    def start(self):
        root.title("Which component would you like to test?")
        self.Restore()

    #logic for handling the even when test button is presed 
    def test(self):
        root.title("Starting Device")
        self.Restore()

        #creating the buttons for test
        self.test_FeederBowl = Button(text="Vibrating Feeder Bowl", height=2, width=20, command=self.feederBowl)
        self.test_Rerolling = Button(text="Rerolling Assembly", height=2, width=20, command=self.rerolling)
        self.test_ClearCover = Button(text="Clear Cover Remover", height=2, width=20, command=self.clearCover)
        self.test_PickPlace = Button(text="Pick and Place", height=2, width=20, command=self.pickPlace)
        self.test_Pump = Button(text="Pump", height=2, width=20, command=self.pump)
        self.back_button = Button(text="Back", height=2, width=9, command=self.back)

        #displaying buttons in GUI
        self.test_FeederBowl.place(relx=0.1, rely=0.2, anchor=NW)
        self.test_Rerolling.place(relx=0.1, rely=0.3, anchor=NW)
        self.test_ClearCover.place(relx=0.1, rely=0.4, anchor=NW)
        self.test_PickPlace.place(relx=0.1, rely=0.5, anchor=NW)
        self.test_Pump.place(relx=0.1, rely=0.6, anchor=NW)
        self.back_button.place(relx=0.1, rely=.9, anchor=NW)

    #this function remove all the widgets(buttons)
    def Restore(self):
            for widgets in root.winfo_children():
                widgets.destroy()
    #the following 4 function display the message box when one of the text buttons is clicked           
    def feederBowl(self):
        #message box that display the message we want, change text to change message
        #messagebox.askyesno("Test Feeder Bowl", "This action will turn on the feeder bowl for 1 minute. Do you wish to proceed?")
        channel = 11
        GPIO.setup(channel,GPIO.OUT)
        try:
            GPIO.output(channel, GPIO.HIGH) #turns pump on
            time.sleep(3)
            GPIO.output(channel, GPIO.LOW) #turns pump off
            time.sleep(3)
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD)
        except KeyboardInterrupt:
            GPIO.cleanup()
                           
    def rerolling(self):
        #git repository for the motor sheild https://github.com/sbcshop/MotorShield.git
        #messagebox.askyesno("Test Feeder Bowl", "This action will produce one full revolution of the sticky pad roller. Do you wish to proceed?")
        #assignes the stepper motors i.e stepper 2 takes up motor 3 and motor 4 slots 
        m1 = PiMotor.Stepper("STEPPER1")

        # Rotate Stepper 1 in forward/backward direction
        try:
            m1.forward(0.05,20)  # Delay and rotations
            time.sleep(1)
            m1.backward(0.05,20)
            time.sleep(1)

        except KeyboardInterrupt:
            GPIO.cleanup()

    def clearCover(self):
        #git repository for the motor sheild https://github.com/sbcshop/MotorShield.git
        #messagebox.askyesno("Test Feeder Bowl", "This action will produce one full revolution of the clear cover. Do you wish to proceed?")
        #assignes the stepper motors i.e stepper 2 takes up motor 3 and motor 4 slots 
        m1 = PiMotor.Stepper("STEPPER2")

        # Rotate Stepper 2 in forward/backward direction
        try:
            m1.forward(0.05,20)  # Delay and rotations
            time.sleep(1)
            m1.backward(0.05,20)
            time.sleep(1)

        except KeyboardInterrupt:
            GPIO.cleanup()
       
    def pickPlace(self):
        #messagebox.askyesno("Test Feeder Bowl", "This action will rotate the pick and place twice and away from the track. Do you wish to proceed?")
        GPIO.setup(13, GPIO.OUT)
        pwm = GPIO.PWM(13, 100)
        pwm.start(5)
        
        for x in range(180):
            duty = float(x) / 10.0 + 2.5
            time.sleep(.01)
            pwm.ChangeDutyCycle(duty)
        
    def pump(self):
        channel = 16
        GPIO.setup(channel,GPIO.OUT)
        try:
            GPIO.output(channel, GPIO.HIGH) #turns pump on
            time.sleep(3)
            GPIO.output(channel, GPIO.LOW) #turns pump off
            time.sleep(3)
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD)
        except KeyboardInterrupt:
            GPIO.cleanup()

    #when back button is pressed we delete all widgets and call the contructor to displayed our previos window
    def back(self):
        self.Restore()
        self.__init__(root)


root = Tk()

run = Window(root)

root.mainloop()
