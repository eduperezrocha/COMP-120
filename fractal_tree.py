"""
File: fractal_tree.py
Author: Eduardo Pérez
Date:3/31/22
Description: Displays fractal tree
"""
import tkinter as tk
import math
class FractalTree:
    def __init__(self):
        """ Initialize the fractal object. """

        #instance variables
        self.window = tk.Tk()
        self.canvas_width = 400
        self.canvas_height = 400
        self.button_Width = 14
        self.child_branch = 0.58
        self.level = 0
        self.angle = math.pi/2
        self.x_1 = self.canvas_width//2
        self.y_1 = self.canvas_height - 20


    #make the canvas
        self.canvas = tk.Canvas(self.window, 
                width = self.canvas_width,
                height = self.canvas_height,
                bg = 'white')
        self.canvas.grid(row=1,column=1) 

        #Buttons created
        self.button_Frame = tk.Frame(self.window,width=self.canvas_width,height=self.canvas_height)
        self.button_Frame.grid(row=2,column=1)
        
        self.advance_button = tk.Button(self.button_Frame, bg = 'white', command = self.advance, text = 'Advance',width = self.button_Width)
        self.advance_button.grid(row=2,column=1)

        self.reset_button = tk.Button(self.button_Frame, bg = 'white', command = self.reset, text = 'Reset',width = self.button_Width)
        self.reset_button.grid(row=2,column=2)

        self.quit_button = tk.Button(self.button_Frame, bg = 'white', command = self.quit, text = 'Quit',width = self.button_Width)
        self.quit_button.grid(row=2,column=3)

        self.build_tree(self.level,self.x_1,self.y_1,self.angle, self.canvas_height//3)
                        
        self.window.mainloop()

    def advance(self):
        """"Move forward on more level of recursion"""
        self.level = self.level + 1
        self.build_tree(self.level,self.x_1,self.y_1,self.angle, self.canvas_height//3)
   
    def reset(self):
        """Delte everything drawn"""
        self.level = 0
        self.canvas.delete("all")
        self.build_tree(self.level,self.x_1,self.y_1,self.angle, self.canvas_height//3)
   
    def quit(self):
        """Terminate program"""
        self.window.destroy()

    def build_tree(self,level,x,y,angle,len):
        """input: self, int: level of recursion, double: x index of base branch, double: y index of base branch, double: angle radius, double: length of branch
        create a layer of lines in the tree """
        #base case
        if level < 0:
            return

        #recursive case
        else:
            new_x_2 =  x + int(math.cos(angle)*len) 
            new_y_2 = y - int(math.sin(angle)*len)
            self.canvas.create_line(x,y,new_x_2,new_y_2)
        
        #next fractals
            self.build_tree(level - 1, new_x_2,new_y_2,angle+math.pi/5,len*self.child_branch)
            self.build_tree(level - 1, new_x_2,new_y_2,angle-math.pi/5,len*self.child_branch)
    
if __name__ == "__main__":
    FractalTree()