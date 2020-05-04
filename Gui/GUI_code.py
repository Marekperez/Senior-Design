from tkinter import *
import tkinter as tk
from tkinter import messagebox
import PiMotor
import time
import VL53L0X
import RPi.GPIO as GPIO
from subprocess import call
import threading

#global boolian variable for start while loop
start = False       
#vibrating feeder bowl pin 
VF = 11
#vibrating feeder bowl pin 
Pump = 16
#pwm for servo pin
PWM = 13


class page2:
    def stop(self):
        start = False
        GPIO.setup(VF,GPIO.OUT)
        GPIO.setup(Pump,GPIO.OUT)
        GPIO.output(Pump, GPIO.HIGH)
        GPIO.output(VF, GPIO.LOW)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        self.Restore()
        self.__init__(root)




class Window:

    def __init__(self, master):

        #size of user interface
        root.geometry("600x600")
        root.title("Automated iButton Device GUI")

        #creating the buttons, the command atribute calls the function
        self.start_button = Button(master, text="Start System", height=2, width=12, bd=3, command=lambda: self.start(master) )
        self.test_button = Button(master, text="Test Component", height=2, width=12, bd=3, command=self.test)
        self.stop_button = Button(master, text="Stop", height=2, width=12, bd=3, command = self.stop)

        #displaying the buttons in the GUI, change relx and rely to move buttons around
        self.start_button.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.test_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.stop_button.place(relx=0.5, rely=0.7, anchor=CENTER)

    #stars the main machine        
    def start(self, master):
        root.title("Starting")
        self.Restore()
        
        #creates a stop button
        self.stop2_button = Button(master, text="Stop", height=2, width=20, command= self.stop1)
        self.stop2_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        #splits the threads to allow th buton and the code to run in parallel
        thread =threading.Thread(target = self.runit)
        thread.start()

    
    def runit(self):
        start = True

        #this flag says the servo is 90 degrees
        flag = 1
        #rerolling stepper motor
        m1 = PiMotor.Stepper("STEPPER2")
        # Create a VL53L0X object
        tof = VL53L0X.VL53L0X()
        # Start ranging
        tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        #sets up the pump and vibrating feeder bowl pins to be outputs
        
        GPIO.setup(VF,GPIO.OUT)
        GPIO.setup(Pump,GPIO.OUT)
        
        try:
            GPIO.output(Pump, GPIO.LOW) #turns pump on
        except KeyboardInterrupt:
            GPIO.cleanup()
        
        #sets up the pin for the pwm
        GPIO.setup(PWM, GPIO.OUT)
        #initializes the pwm pin to a frequency of 50Hz 
        pwm = GPIO.PWM(PWM, 50)
        #starts the pwm with a 0% duity cicle
        pwm.start(0)
            
        timing = tof.get_timing()
        if (timing < 20000):
            timing = 20000
        
        while start == True:
            distance = tof.get_distance()
            #sleeps long enough to get the range 
            time.sleep(timing/1000000.00)
            
            if (distance  > 50):
                #if the distanse is over a certain amount then the vibrating feeder bowl turns on 
                GPIO.output(VF, GPIO.HIGH)
            else:
                #if the distance is below an amount then the pump turns on and the machine runs
                GPIO.output(VF, GPIO.LOW)
                #moves both stepper motors at the same time
                m1.forward(0.025,10)  # Delay and rotations
                #sleeps while the stepper motors move 
                time.sleep(2)
                #moves the stepermotor from the middle to the right then to pick up a button 
                pwm.ChangeDutyCycle(4)
                time.sleep(1)
                pwm.ChangeDutyCycle(0)
                time.sleep(1)
                #once button is grabbed then the servo moves all the way righ to place it
                pwm.ChangeDutyCycle(11)
                time.sleep(1)
                pwm.ChangeDutyCycle(0)
                time.sleep(1)
                #then the servo moves back to the center 
                pwm.ChangeDutyCycle(7.5)
                time.sleep(1)
                pwm.ChangeDutyCycle(0)
                time.sleep(1)
                
     
    #stops the machine
    def stop1(self):
        start = False
        #sets all the pins to low 
        GPIO.setup(VF,GPIO.OUT)
        GPIO.setup(Pump,GPIO.OUT)
        GPIO.output(Pump, GPIO.HIGH)
        GPIO.output(VF, GPIO.LOW)
        #clears the pins 
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        self.Restore()
        self.__init__(root)
    
        
    def stop(self):
        #shuts down the pi when the stop button is pressed
        call("sudo shutdown -h now", shell = True)

    #logic for handling the even when test button is presed 
    def test(self):
        root.title("Starting Device")
        self.Restore()

        #creating the buttons for test
        self.test_FeederBowl = Button(text="Vibrating Feeder Bowl", height=2, width=20, command=self.feederBowl)
        self.test_RerollClear = Button(text="Reroller and Clear Cover", height=2, width=20, command=self.rerollclear)
        self.test_PickPlace = Button(text="Pick and Place", height=2, width=20, command=self.pickPlace)
        self.test_Pump = Button(text="Pump", height=2, width=20, command=self.pump)
        self.back_button = Button(text="Back", height=2, width=9, command=self.back)

        #displaying buttons in GUI
        self.test_FeederBowl.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.test_RerollClear.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.test_PickPlace.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.test_Pump.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.back_button.place(relx=0.5, rely=.8, anchor=CENTER)

    #this function remove all the widgets(buttons)
    def Restore(self):
            for widgets in root.winfo_children():
                widgets.destroy()
    #the following 4 function display the message box when one of the text buttons is clicked           
    def feederBowl(self):
        #message box that display the message we want, change text to change message
        #messagebox.askyesno("Test Feeder Bowl", "This action will turn on the feeder bowl for 1 minute. Do you wish to proceed?")
        GPIO.setup(VF,GPIO.OUT)
        try:
            GPIO.output(VF, GPIO.HIGH) #turns pump on
            time.sleep(3)
            GPIO.output(VF, GPIO.LOW) #turns pump off
            time.sleep(.5)
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD)
        except KeyboardInterrupt:
            GPIO.cleanup()
                           
    def rerollclear(self):
        #git repository for the motor sheild https://github.com/sbcshop/MotorShield.git
        #messagebox.askyesno("Test Feeder Bowl", "This action will produce one full revolution of the sticky pad roller. Do you wish to proceed?")
        #assignes the stepper motors i.e stepper 2 takes up motor 3 and motor 4 slots 
        m1 = PiMotor.Stepper("STEPPER2")

        # Rotate Stepper 1 in forward/backward direction
        try:
            m1.forward(0.025,20)  # Delay and rotations
            time.sleep(1)
            m1.backward(0.025,20)
            time.sleep(1)

        except KeyboardInterrupt:
            GPIO.cleanup()
       
    def pickPlace(self):
        #messagebox.askyesno("Test Feeder Bowl", "This action will rotate the pick and place twice and away from the track. Do you wish to proceed?")
        GPIO.setup(PWM, GPIO.OUT)
        pwm = GPIO.PWM(PWM, 50)
        pwm.start(0)
        
        #moves the stepermotor from the middle to the right then to pick up a button 
        pwm.ChangeDutyCycle(4)
        time.sleep(1)
        pwm.ChangeDutyCycle(0)
        time.sleep(1)
        #once button is grabbed then the servo moves all the way righ to place it
        pwm.ChangeDutyCycle(11)
        time.sleep(1)
        pwm.ChangeDutyCycle(0)
        time.sleep(1)
        #then the servo moves back to the center 
        pwm.ChangeDutyCycle(7.5)
        time.sleep(1)
        pwm.ChangeDutyCycle(0)
        time.sleep(1)
        

    def pump(self):
        GPIO.setup(Pump,GPIO.OUT)
        try:
            GPIO.output(Pump, GPIO.HIGH) #turns pump on
            time.sleep(.5)
            GPIO.output(Pump, GPIO.LOW) #turns pump off
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
