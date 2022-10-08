# File: addressbook.py
# Author: Eduardo Pérez
# Date: 3/18/2022
# Description: Display a clock with two buttons that stop and continue the timer.

import math 
import datetime
import tkinter as tk
from turtle import update
import time

class Display_Clock:
    def __init__(self):
        """
        Constructor for Display_Clock class
        """
        self.window = tk.Tk() # Create a window
        self.window.title("Clock") # Set a title
        self.canvas_width = 200
        self.frame_height = 200
        self.canvas_height = 200
        self.button_width=8
        self.radius_percentage = 0.8
        self.radius = self.radius_percentage * 0.5 * self.canvas_width
        self.cur_angle = math.radians(360)
        self.counter_second, self.counter_minute, self.counter_hour = 0,0,0
        
        
        #Create Canvas
        self.canvas = tk.Canvas(self.window, 
                width = self.canvas_width,
                height = self.canvas_height,
                bg = 'white') 
        self.canvas.grid(row = 1, column = 1)
        
        #Create buttons and place them in a frame
        self.button_frame= tk.Frame(self.window, width=self.canvas_width, height = self.frame_height)
        self.button_frame.grid(row=2, column=1, sticky='W')
        
        #Clock Circle
        self.color = self.canvas.create_oval(self.canvas_width // 2 - self.radius, self.canvas_height // 2 - self.radius, self.canvas_width // 2 + self.radius, self.canvas_height // 2 + self.radius, fill = "white")
        
        #Numbers in the clock face
        self.hours_text = self.canvas.create_text(self.canvas_width // 2 + self.radius - 5, self.canvas_height // 2, text = 3, fill = "black")
        self.hours_text = self.canvas.create_text(self.canvas_width //  2 - self.radius + 5, self.canvas_height // 2, text = 6, fill = "black")
        self.hours_text = self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + self.radius - 6, text = 9, fill = "black")
        self.hours_text = self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 - self.radius + 6, text = 12, fill = "black")
        
        #
        self.start_button = tk.Button(self.button_frame, bg = 'white', command = self.start,
                                        text = "Stop", width=self.button_width)
        self.start_button.grid(row = 1, column = 1, padx = (30,2),pady=5)

        self.quit_button = tk.Button(self.button_frame, bg = 'white', command = self.quit,
                                        text = "Quit", width=self.button_width)
        self.quit_button.grid(row = 1, column = 2, padx =(2,30), pady=5)

        #Display Timer
        self.display_timer = self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + self.radius + 7, text = time.strftime("%H:%M:%S"))
        self.time_display()
 
        self.window.mainloop()

    def time_display(self):
        """Displays the hands and the digital timer for the clock"""
        #Get actual time in str
        now = time.strftime("%H:%M:%S")
        self.canvas.itemconfig(self.display_timer, text=now)
       
        #Checks if the user did not hit stop button
        if self.start_button['text'] == 'Stop':
            self.canvas.delete('hands')
            current_time = datetime.datetime.now()
            
            #Get angle Hours
            self.cur_angle_hr = math.radians((((current_time.hour % 12) * 360) //12 + (current_time.minute * 360)//(12 * 60)-90))
           
            #Get angle Minutes
            self.cur_angle_min = math.radians(((current_time.minute * 360) // 60)-90)
           
            #Get angle Seconds
            self.cur_angle_sec = math.radians(((current_time.second * 360) // 60)-90)
           
            #Second Hand
            self.x_cord_second = ((self.canvas_width //2) + (self.radius * 0.8) * math.cos(self.cur_angle_sec))
            self.y_cord_second = ((self.canvas_height//2) + (self.radius * 0.8) * math.sin(self.cur_angle_sec))
            self.second_hand = self.canvas.create_line(self.canvas_width //2,self.canvas_height//2, self.x_cord_second, self.y_cord_second,fill = "red", tag="hands")

            #Minute Hand
            self.x_cord_minute = ((self.canvas_width //2) + (self.radius * 0.65) * math.cos(self.cur_angle_min))
            self.y_cord_minute = ((self.canvas_height//2) + (self.radius * 0.65) * math.sin(self.cur_angle_min))
            self.minute_hand = self.canvas.create_line(self.canvas_width //2,self.canvas_height//2, self.x_cord_minute, self.y_cord_minute,fill = "blue",tag="hands")


            #Hour Hand
            self.x_cord_hour = ((self.canvas_width //2) + (self.radius * 0.5) * math.cos(self.cur_angle_hr))
            self.y_cord_hour = ((self.canvas_height//2) + (self.radius * 0.5) * math.sin(self.cur_angle_hr))
            self.hour_hand = self.canvas.create_line(self.canvas_width //2,self.canvas_height//2, self.x_cord_hour, self.y_cord_hour,fill = "green",tag="hands")
            self.window.after(1000, self.time_display)
        else:
            pass
        
    
    
    def start(self):
        """Changes the buttons text and callls the time display to stop"""
        if self.start_button['text'] == 'Stop':
            self.start_button['text'] = 'Start'
        else:
            self.start_button['text'] = 'Stop'
            self.time_display()
    
    def quit(self): 
        """Exits the program"""
        self.window.destroy()

if __name__ == "__main__":
    Display_Clock()
