"""
File: wordy.py
Authors: Francisco Monarrez and Eduardo Perez
Date: 04/28/2022
Description: A Python/tkinter implementation of wordle.
"""

# Imports
from cgitb import reset
import random
import tkinter as tk
import tkinter.font as font
from enum import Enum
import time
from numpy import corrcoef, row_stack
from functools import reduce
import operator

class Wordy:
    def __init__(self):
        # Create window
        self.window = tk.Tk()
        self.window.title("Wordy")

        """ Initialize the game """
        # Constants
        self.WORD_SIZE = 5  # number of letters in the hidden word
        self.NUM_GUESSES = 6 # number of guesses that the user gets 
        self.LONG_WORDLIST_FILENAME = "long_wordlist.txt"
        self.SHORT_WORDLIST_FILENAME = "short_wordlist.txt"
        self.PADDING = 10 # Padding around widgets
        self.ENTRY_SIZE = 10 # Size of entry widget
        self.FONT_FAMILY = 'ariel'
        self.FONT = font.Font(family=self.FONT_FAMILY)

        # Size of the frame that holds all guesses.  This is the upper left
        # frame in the window.
        self.PARENT_GUESS_FRAME_WIDTH = 750
        self.PARENT_GUESS_FRAME_HEIGHT = 500

        #Initialize row_squares and column_squares equal to zero
        self.row_squares = 0
        self.column_squares = 0
        self.current_row_game = 0
        
        #Set start_button_bool and guess_frame_full equal to False
        self.start_button_bool = False
        self.guess_frame_full = False

        #Initialize lists
        self.words_long = []
        self.words_short = []
        self.guess_labels_list=[]
        self.word_guesslist=[]
        self.frame_guess_list = [[],[],[],[],[],[]]
        self.correct_letters = {0:[], 1:[], 2:[], 3:[], 4:[]}
        self.letters_used_incorrect = {0:[],1:[],2:[],3:[],4:[]}
        self.letters_used_incorrect_flat = [] #For checking flat list
        self.letters_used_yellow = {0:[],1:[],2:[],3:[],4:[]}
        self.letters_used_yellow_flat = [] 
        


        # Parameters for an individual letter in the guess frame
        # A guess frame is an individual box that contains a guessed letter.
        self.GUESS_FRAME_SIZE = 50  # the width and height of the guess box.
        self.GUESS_FRAME_PADDING = 2 
        self.GUESS_FRAME_BG_BEGIN = 'white' # background color of a guess box 
                                            # after the user enters the letter,
                                            # but before the guess is entered.
        self.GUESS_FRAME_TEXT_BEGIN = 'black' # color of text in guess box after the
                                            # user enters the letter, but before
                                            # the guess is entered.
        self.GUESS_FRAME_BG_WRONG = 'grey'  # background color of guess box
                                            # after the guess is entered, and the
                                            # letter is not in the hidden word.
        self.GUESS_FRAME_BG_CORRECT_WRONG_LOC = 'orange' # background color
                                            # guess box after the guess is entered
                                            # and the letter is in the hidden word
                                            # but in the wrong location.
        self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC = 'green' # background color
                                            # guess box after the guess is entered
                                            # and the letter is in the hidden word
                                            # and in the correct location.
        self.GUESS_FRAME_TEXT_AFTER = 'white' # color of text in guess box after
                                            # the guess is entered.
        self.FONT_FAMILY = 'ariel'          # Font to use for letters in the guess boxes.
        self.FONT_SIZE_GUESS = 35           # Font size for letters in the guess boxes.

        # Parameters for the keyboard frame
        self.KEYBOARD_FRAME_HEIGHT = 200
        self.KEYBOARD_BUTTON_HEIGHT = 2
        self.KEYBOARD_BUTTON_WIDTH = 3  # width of the letter buttons.  Remember,
                                        # width of buttons is measured in characters.
        self.KEYBOARD_BUTTON_WIDTH_LONG = 5 # width of the enter and back buttons.

        # The following colors for the keyboard buttons
        # follow the same specifications as the colors defined above for the guess
        # boxes.  The problem is that if one or both of you have a mac, you will
        # not be able to change the background color of a button.  In this case,
        # just change the color of the text in the button, instead of the background color.
        # So the text color starts as the default (black), and then changes to grey, orange, 
        # green depending on the result of the guess for that letter.
        self.KEYBOARD_BUTTON_BG_BEGIN = 'white' 
        self.KEYBOARD_BUTTON_TEXT_BEGIN = 'black' 
        self.KEYBOARD_BUTTON_BG_WRONG = 'grey'  
        self.KEYBOARD_BUTTON_BG_CORRECT_WRONG_LOC = 'orange' 
        self.KEYBOARD_BUTTON_BG_CORRECT_RIGHT_LOC = 'green' 
        self.KEYBOARD_BUTTON_TEXT_AFTER = 'white' 

        self.KEYBOARD_BUTTON_NAMES = [   
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "BACK"]]
        
        # Parameters for the control frame
        self.CONTROL_FRAME_HEIGHT = self.PARENT_GUESS_FRAME_HEIGHT + self.KEYBOARD_FRAME_HEIGHT
        self.CONTROL_FRAME_WIDTH = 300
        self.USER_SELECTION_PADDING = 10  # Horizontal padding on either side of the widgets in
                                            # the parameter frame.

        self.MESSAGE_DISPLAY_TIME_SECS = 5 # Length of time the message should be
                                            # displayed.
        self.PROCESS_GUESS_WAITTIME = 1  # When processing a guess (changing color
                                        # of the guess frames), time to wait between
                                        # updating successive frames.

        # Create a guess_frame  as the upper top frame.
        self.guess_frame = tk.Frame(self.window, 
            borderwidth = 1, relief = 'solid',
            height = self.PARENT_GUESS_FRAME_HEIGHT, 
            width = self.PARENT_GUESS_FRAME_WIDTH)
        self.guess_frame.grid(row = 1, column = 1)
        self.guess_frame.grid_propagate(False)

        # Create a keyboard_frame as the lower left frame.
        self.keyboard_frame = tk.Frame(self.window, 
            borderwidth = 1, relief = 'solid',
            height = self.KEYBOARD_FRAME_HEIGHT, width = self.PARENT_GUESS_FRAME_WIDTH)
        self.keyboard_frame.grid(row = 2, column = 1)
        self.keyboard_frame.grid_propagate(False)

        # Create a control_frame as the right frame.
        self.control_frame = tk.Frame(self.window, 
            height = self.CONTROL_FRAME_HEIGHT, width = self.CONTROL_FRAME_WIDTH)
        self.control_frame.grid(row = 1, column = 2, rowspan = 3)
        self.control_frame.grid_propagate(False)

        # Create a message_frame as the upper frame inside control_frame.
        self.message_frame = tk.Frame(self.control_frame, 
            borderwidth = 1, relief = 'solid',
            height = self.CONTROL_FRAME_HEIGHT//3, width = self.CONTROL_FRAME_WIDTH)
        self.message_frame.grid(row = 1, column = 2)
        self.message_frame.grid_propagate(False)

        # Create a parameter_frame as the middle frame inside control_frame.
        self.parameter_frame = tk.Frame(self.control_frame, 
            borderwidth = 1, relief = 'solid',
            height = self.CONTROL_FRAME_HEIGHT//3, width = self.CONTROL_FRAME_WIDTH)
        self.parameter_frame.grid(row = 2, column = 2)
        self.parameter_frame.grid_propagate(False)
        
        # Create a button_frame as the low frame inside control_frame.
        self.button_frame = tk.Frame(self.control_frame, 
            borderwidth = 1, relief = 'solid',
            height = self.CONTROL_FRAME_HEIGHT//3, width = self.CONTROL_FRAME_WIDTH)
        self.button_frame.grid(row = 3, column = 2)
        self.button_frame.grid_propagate(False)

                # Start event loop
        # Put a button in the bottom frame
        self.start_button  = tk.Button(self.button_frame, text = "Start Game", command = self.check_errors)
        #self.start_button.pack(side=tk.RIGHT,expand=True)
        self.start_button.grid(row = 1, column = 1)


        # Put a button in the bottom frame
        self.quit_button  = tk.Button(self.button_frame, text = "Quit", command=self.quit)
        #self.quit_button.pack(side=tk.RIGHT, expand=True)
        self.quit_button.grid(row = 1, column = 2)

        # Center the button in its frame
        self.button_frame.grid_rowconfigure(1, weight = 1)
        self.button_frame.grid_columnconfigure(3, weight = 1)
        self.button_frame.grid_columnconfigure(0, weight = 1)

         # Put a checkbox in the top frame.  Make the default
         # on.
        self.hardmode_var = tk.BooleanVar()
        self.hardmode_var.set(False)
        self.hardmode = tk.Checkbutton(self.parameter_frame, text="Hard mode", 
                            var = self.hardmode_var)
        self.hardmode.grid(row = 1, column = 1, sticky = tk.W, padx = self.USER_SELECTION_PADDING)

        # Put a checkbox in the top frame.  Make the default
         # on.
        self.guesses_var = tk.BooleanVar()
        self.guesses_var.set(True)

        self.game_over = False

        self.hidden_word = tk.StringVar()
    
        self.guesses = tk.Checkbutton(self.parameter_frame, text="Guesses must be words", 
                            var = self.guesses_var, onvalue=True, offvalue=False)
        self.guesses.grid(row = 2, column = 1, sticky = tk.W, padx = self.USER_SELECTION_PADDING)

        # Put a checkbox in the top frame.  Make the default
         # on.
        self.showword_var = tk.BooleanVar()
        self.showword_var.set(False)
        self.show_word = tk.Checkbutton(self.parameter_frame, text="Show word", 
                            var = self.showword_var, onvalue=True, offvalue=False, command=self.show_hidden_word)
        self.show_word.grid(row = 3, column = 1, sticky = tk.W, padx = self.USER_SELECTION_PADDING)

        self.show_word_label = tk.Label(self.parameter_frame, textvariable=self.hidden_word)

        # Put a checkbox in the top frame.  Make the default
         # on.
        self.specifyword_var = tk.BooleanVar()
        self.specifyword_var.set(False)
        self.specify_word = tk.Checkbutton(self.parameter_frame, text="Specify word", 
                            var = self.specifyword_var, onvalue=True, offvalue=False)
        self.specify_word.grid(row = 4, column = 1, sticky = tk.W, padx = self.USER_SELECTION_PADDING)

        # Put an entry widget to the right
        self.entry_var = tk.StringVar()
        self.entry  = tk.Entry(self.parameter_frame, textvariable=self.entry_var, width = self.WORD_SIZE)
        self.entry.grid(row = 4, column=2, padx = self.WORD_SIZE)

        #Shows Label Error
        self.error_message = tk.StringVar()
        self.error_label = tk.Label(self.message_frame, textvariable=self.error_message)

        # Center the frame in the window
        self.window.rowconfigure(0, weight = 1)
        self.window.rowconfigure(2, weight = 1)
        self.window.columnconfigure(0, weight = 1)
        self.window.columnconfigure(2, weight = 1)

        #Keyboard
        # Define text to go in the buttons
        self.buttons = {}
        self.squares_guess={}

        #Create keyboardframe and guessframe
        self.setup_keyboardframe()
        self.setup_guessframe()
        self.grid_rowandcolumn()
        self.longwordlist()
        self.shortwordlist()

        self.window.mainloop()

    def grid_rowandcolumn(self):
        """
        Grid rows and columns from message_frame and parameter_frame
        """
        self.message_frame.grid_rowconfigure(0, weight = 1)
        self.message_frame.grid_columnconfigure(0, weight = 1)
        self.message_frame.grid_rowconfigure(2, weight = 1)
        self.message_frame.grid_columnconfigure(2, weight = 1)

        # Center the button in its frame
        self.parameter_frame.grid_rowconfigure(0, weight = 1)
        self.parameter_frame.grid_rowconfigure(5, weight = 1)

    def setup_guessframe(self):
        """
        Creates guess_frame
        """
        #Creates list of lists for every square
        self.guess_frame_squares = [   
            ["", "", "", "", ""],["", "", "", "", ""],
            ["", "", "", "", ""],["", "", "", "", ""],
            ["", "", "", "", ""],["", "", "", "", ""]]
        #Create squares in guess frame
        for r in range(len(self.guess_frame_squares)):
            for c in range(len(self.guess_frame_squares[r])):
                square_guess = tk.Frame(self.guess_frame, borderwidth = 1, relief = 'solid',
                        width = self.GUESS_FRAME_SIZE, height=self.GUESS_FRAME_SIZE,bg = self.GUESS_FRAME_BG_BEGIN)
                square_guess.grid(row = r + 1, column = c + 1, padx=self.GUESS_FRAME_PADDING, 
                pady=self.GUESS_FRAME_PADDING)
                self.frame_guess_list[r].append(square_guess)

                # Put the square in a dictionary of squares
                # where the key is the button text, and the
                # value is the button object.
                self.squares_guess[self.guess_frame_squares[r][c]] = square_guess

        # Center the grid of buttons in the button frame
        self.guess_frame.rowconfigure(0, weight = 1)
        self.guess_frame.rowconfigure(len(self.guess_frame_squares) + 1, weight = 1)
        self.guess_frame.columnconfigure(0, weight = 1)
        self.guess_frame.columnconfigure(len(self.guess_frame_squares[0]) + 1, weight = 1)

    def setup_keyboardframe(self):
        """
        Creates keyboard_frame with buttons for every letter
        """
        for r in range(len(self.KEYBOARD_BUTTON_NAMES)):
            # Create a keyboard_frame as the lower left frame.
            #Checks if it is the first or last frame
            if r==0 or r ==2:
                self.innerkeyboard_frame = tk.Frame(self.keyboard_frame, 
                    height = self.KEYBOARD_FRAME_HEIGHT//3, width = self.PARENT_GUESS_FRAME_WIDTH)
                self.innerkeyboard_frame.grid(row = r, column = 0)
                self.innerkeyboard_frame.grid_propagate(False)
                self.innerkeyboard_frame.columnconfigure(0, weight = 1)
            #Checks if it is the middle frame
            if r==1:
                self.innerkeyboard_frame = tk.Frame(self.keyboard_frame, 
                    height = 30, width = self.PARENT_GUESS_FRAME_WIDTH)
                self.innerkeyboard_frame.grid(row = r, column = 0)
                self.innerkeyboard_frame.grid_propagate(False)
                self.innerkeyboard_frame.columnconfigure(0, weight = 1)
            #Create the buttons.
            for c in range(len(self.KEYBOARD_BUTTON_NAMES[r])):
                def handler(key = self.KEYBOARD_BUTTON_NAMES[r][c]):
                    self.button_handler(key)
                size = self.KEYBOARD_BUTTON_WIDTH
                if self.KEYBOARD_BUTTON_NAMES[r][c] == "ENTER" or self.KEYBOARD_BUTTON_NAMES[r][c] == "BACK":
                    size = self.KEYBOARD_BUTTON_WIDTH_LONG
                button = tk.Button(self.innerkeyboard_frame,
                        width = size,
                        text = self.KEYBOARD_BUTTON_NAMES[r][c],
                        bg=self.KEYBOARD_BUTTON_BG_BEGIN, 
                        font=self.FONT,
                        command = handler)
                button.grid(row = r + 1, column = c + 1)

                # Put the button in a dictionary of buttons
                # where the key is the button text, and the
                # value is the button object.
                self.buttons[self.KEYBOARD_BUTTON_NAMES[r][c]] = button
            # Center the grid of buttons in the button frame
            if r == 0:
                self.innerkeyboard_frame.rowconfigure(0, weight = 1)
            self.innerkeyboard_frame.columnconfigure(len(self.KEYBOARD_BUTTON_NAMES[0]) + 1, weight = 1)

    def button_handler(self, text):
        """
        If text is equals to back or enter calls to the their buttons functions
        Else adds letter to the corresponding frame
        """
        print(text)
        if text == 'BACK' and self.start_button_bool == True:
            try:
                self.back_button()
            except IndexError:
                pass
        elif text == 'ENTER' and self.start_button_bool == True:
                self.enter_button()
        elif self.guess_frame_full != True and self.start_button_bool == True and self.game_over == False:
            self.column_squares = len(self.guess_labels_list)
            letter = text
            self.guess_frame_squares[self.row_squares][self.column_squares] = letter
            self.letter_label = tk.Label(self.guess_frame, text=letter, font=(self.FONT, self.FONT_SIZE_GUESS), bg= 'white', fg='black')
            self.letter_label.grid(row=self.row_squares+1,column=self.column_squares+1, padx=self.GUESS_FRAME_PADDING, 
                    pady=self.GUESS_FRAME_PADDING)
            self.guess_labels_list.append(self.letter_label)
            text = text.lower()
            self.word_guesslist.append(text)
            self.current_label=self.letter_label
            if self.column_squares==4:
                self.column_squares=4
                self.guess_frame_full = True
            if self.row_squares==6:
                self.row_squares=0
           
    def enter_button(self):
        """
        Goes to the next line if there is no error and checks for errors.
        """
        current_guess_word = ""
        #Loop through the guessed word and check every character
        for i in range(len(self.word_guesslist)):
                current_guess_word += f"{self.word_guesslist[i]}"
        if not self.game_over:
            if len(self.word_guesslist) < 5 and self.game_over == False:
                self.display_error_message("Word not finished")
            if current_guess_word != self.hidden_word.get() and self.column_squares ==4 and self.row_squares == 5:
                self.display_error_message("Game Over")
                self.game_over = True #Sets game over
                self.guess_frame_full = True
            elif current_guess_word == self.hidden_word.get() and self.column_squares ==4 and self.row_squares == 5:
                self.guess_frame_full = True
                self.game_over = True
            #Iterates to go to the next line in guess frames and checks for errors 
            if len(self.word_guesslist) == 5 and self.row_squares < 6 and self.game_over== False: 
                if self.guesses_var.get() and self.hardmode_var.get() == False:
                    #Choose random word and assign it 
                    if current_guess_word not in self.words_long:
                        self.display_error_message(f"{current_guess_word} not in the word list")
                    else:
                        self.change_colors_squares1()
                elif self.guesses_var.get()==False and self.hardmode_var.get()==False:
                    self.change_colors_squares2()
        if self.hardmode_var.get():           
            self.check_hardmode()
                
    def change_colors_squares1(self):
        """
        Changes the color of the squares if 
        Guesses must be words is checked
        """
        #Initialize variables
        self.correct_word = str(self.hidden_word.get())
        self.correct_word.lower()
        correct_word_lst = []
        correct_list_yellow = []
        for i in range(len(self.correct_word)):
            correct_word_lst.append(self.correct_word[i])
            correct_list_yellow.append(self.correct_word[i])
        current_guess_word = ""
        #Loop through the guessed word and check every character
        for i in range(len(self.word_guesslist)):
                current_guess_word += f"{self.word_guesslist[i]}"
                if self.word_guesslist[i] == self.correct_word[i]:
                    correct_list_yellow.remove(self.word_guesslist[i])
        #Initialize more variables
        current_guess_word = current_guess_word.lower()
        correct = 0
        for i in range(len(correct_word_lst)):
            if self.word_guesslist[i] == correct_word_lst[i]:
                #Turns in green if letter right and in right order
                time.sleep(self.PROCESS_GUESS_WAITTIME)  #Waits 1 second
                self.window.update()
                self.frame_guess_list[self.row_squares][i].config(bg = self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC)
                self.guess_labels_list[i]['bg']=self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC
                self.guess_labels_list[i]['fg']=self.GUESS_FRAME_TEXT_AFTER
                button_text= current_guess_word.upper()
                self.buttons[button_text[i]]['fg'] = self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC
                correct += 1
                if correct == 5:
                    self.display_error_message("Correct. Nice job. Game over.")
                    self.game_over = True
            elif self.word_guesslist[i] in correct_word_lst and self.word_guesslist[i] in correct_list_yellow:
                #Turns in orange if letter right but not right order
                time.sleep(self.PROCESS_GUESS_WAITTIME) #Waits 1 second
                self.window.update()
                self.frame_guess_list[self.row_squares][i].config(bg = self.GUESS_FRAME_BG_CORRECT_WRONG_LOC)
                self.guess_labels_list[i]['bg']=self.GUESS_FRAME_BG_CORRECT_WRONG_LOC
                self.guess_labels_list[i]['fg']= self.GUESS_FRAME_TEXT_AFTER
                button_text= current_guess_word.upper()
                self.buttons[button_text[i]]['fg'] = self.GUESS_FRAME_BG_CORRECT_WRONG_LOC
                correct = 0
                correct_list_yellow.remove(self.word_guesslist[i])
            else:
                #Turns in grey if letter not right
                time.sleep(self.PROCESS_GUESS_WAITTIME) #Waits 1 second
                self.window.update()
                self.frame_guess_list[self.row_squares][i].config(bg = self.GUESS_FRAME_BG_WRONG)
                self.guess_labels_list[i]['bg']=self.GUESS_FRAME_BG_WRONG
                self.guess_labels_list[i]['fg']= self.GUESS_FRAME_TEXT_AFTER 
                button_text= current_guess_word.upper()
                if self.buttons[button_text[i]]['fg'] != "green":
                    self.buttons[button_text[i]]['fg'] = self.GUESS_FRAME_BG_WRONG 
                elif self.buttons[button_text[i]]['fg'] != "green":
                    self.buttons[button_text[i]]['fg'] = self.GUESS_FRAME_BG_WRONG 
                correct = 0  
        #Reset value
        self.reset_values()

    def change_colors_squares2(self):
        """
        Changes the color of the squares if 
        Guesses must be words is not checked
        """
      
        #Initialize variables
        correct_letters = []
        self.correct_word = str(self.hidden_word.get())
        self.correct_word.lower()
        correct_word_lst = []
        correct_list_yellow = []
        for i in range(len(self.correct_word)):
            correct_word_lst.append(self.correct_word[i])
            correct_list_yellow.append(self.correct_word[i])
        current_guess_word = ""
        #Loop through the guessed word and check every character
        count = 0
        for i in range(len(self.word_guesslist)):
                current_guess_word += f"{self.word_guesslist[i]}"
                if self.word_guesslist[i] == self.correct_word[i]:
                    self.one_correct_word = True
                    correct_letters.append(self.word_guesslist[i])
                    correct_list_yellow.remove(self.word_guesslist[i])
        #Initialize more variables
        current_guess_word = current_guess_word.lower()
        correct = 0
        for i in range(len(self.word_guesslist)):
            if self.word_guesslist[i] == correct_word_lst[i]:
                #Turns in green if letter right and in right order
                time.sleep(self.PROCESS_GUESS_WAITTIME) 
                self.window.update()
                self.frame_guess_list[self.row_squares][i].config(bg = self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC)
                self.guess_labels_list[i]['bg']=self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC
                self.guess_labels_list[i]['fg']=self.GUESS_FRAME_TEXT_AFTER
                button_text= current_guess_word.upper()
                self.buttons[button_text[i]]['fg'] = self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC
                correct += 1
                if correct == 5:
                    self.display_error_message("Correct. Nice job. Game over.")
                    self.game_over = True
            elif self.word_guesslist[i] in correct_word_lst and self.word_guesslist[i] in correct_list_yellow:
                #Turns in orange if letter right but not right order
                time.sleep(self.PROCESS_GUESS_WAITTIME)
                self.window.update()
                self.frame_guess_list[self.row_squares][i].config(bg = self.GUESS_FRAME_BG_CORRECT_WRONG_LOC)
                self.guess_labels_list[i]['bg']=self.GUESS_FRAME_BG_CORRECT_WRONG_LOC
                self.guess_labels_list[i]['fg']= self.GUESS_FRAME_TEXT_AFTER
                button_text= current_guess_word.upper()
                self.buttons[button_text[i]]['fg'] = self.GUESS_FRAME_BG_CORRECT_WRONG_LOC
                correct_list_yellow.remove(self.word_guesslist[i])
                correct = 0
                count-=1
            else:
                #Turns in grey if letter not right
                time.sleep(self.PROCESS_GUESS_WAITTIME) 
                self.window.update()
                self.frame_guess_list[self.row_squares][i].config(bg = self.GUESS_FRAME_BG_WRONG)
                self.guess_labels_list[i]['bg']=self.GUESS_FRAME_BG_WRONG
                self.guess_labels_list[i]['fg']= self.GUESS_FRAME_TEXT_AFTER
                button_text= current_guess_word.upper()
                if self.buttons[button_text[i]]['fg'] != "green":
                    self.buttons[button_text[i]]['fg'] = self.GUESS_FRAME_BG_WRONG 
                elif self.buttons[button_text[i]]['fg'] != "green":
                    self.buttons[button_text[i]]['fg'] = self.GUESS_FRAME_BG_WRONG 
                correct = 0  
        #Reset values
        self.reset_values()

    def change_colors_hardmode(self):
        """
        Change the colors of the frame according to what the user guessed
        """
        correct = 0
        self.correct_word = str(self.hidden_word.get())
        current_guess_word = ""
        correct_word_lst = []
        self.correct_word.lower()
        correct_word_lst = []
        hardmode_error = False
        correct_list_yellow = []
        for i in range(len(self.correct_word)):
            correct_word_lst.append(self.correct_word[i])
        current_guess_word = ""
        correct_word_lst = []
        for i in range(len(self.correct_word)):
            correct_word_lst.append(self.correct_word[i])
            correct_list_yellow.append(self.correct_word[i])
        for i in range(len(self.word_guesslist)):
                current_guess_word += f"{self.word_guesslist[i]}"
                if self.word_guesslist[i] == self.correct_word[i]:
                    self.correct_letters[i].append(self.word_guesslist[i])
                    correct_list_yellow.remove(self.word_guesslist[i])
        current_guess_word = current_guess_word.lower()
        self.corr_wor_flat_list = reduce(operator.concat, self.correct_letters.values())
        for i in range(len(self.word_guesslist)):
            if self.word_guesslist[i] == correct_word_lst[i] and self.word_guesslist[i] in self.correct_letters[i]:
                #Turns in green if letter right and in right order
                time.sleep(self.PROCESS_GUESS_WAITTIME) 
                self.window.update()
                self.frame_guess_list[self.row_squares][i].config(bg = self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC)
                self.guess_labels_list[i]['bg']=self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC
                self.guess_labels_list[i]['fg']=self.GUESS_FRAME_TEXT_AFTER
                button_text= current_guess_word.upper()
                self.buttons[button_text[i]]['fg'] = self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC
                correct += 1
                if correct == 5:
                    self.display_error_message("Correct. Nice job. Game over.")
                    self.game_over = True
            elif self.word_guesslist[i] in correct_word_lst and self.word_guesslist[i] in correct_list_yellow:
                #Turns in orange if letter right but not right order
                time.sleep(self.PROCESS_GUESS_WAITTIME)
                self.window.update()
                self.frame_guess_list[self.row_squares][i].config(bg = self.GUESS_FRAME_BG_CORRECT_WRONG_LOC)
                self.guess_labels_list[i]['bg']=self.GUESS_FRAME_BG_CORRECT_WRONG_LOC
                self.guess_labels_list[i]['fg']= self.GUESS_FRAME_TEXT_AFTER
                button_text= current_guess_word.upper()
                self.buttons[button_text[i]]['fg'] = self.GUESS_FRAME_BG_CORRECT_WRONG_LOC
                self.letters_used_yellow_flat.append(self.word_guesslist[i])
                self.letters_used_yellow[i].append(self.word_guesslist[i])
                correct_list_yellow.remove(self.word_guesslist[i])
                correct = 0
            elif self.word_guesslist[i] not in self.letters_used_incorrect[i] and len(self.correct_letters[i]) < 1:
                #Turns in grey if letter not right
                time.sleep(self.PROCESS_GUESS_WAITTIME) 
                self.window.update()
                self.frame_guess_list[self.row_squares][i].config(bg = self.GUESS_FRAME_BG_WRONG)
                self.guess_labels_list[i]['bg']=self.GUESS_FRAME_BG_WRONG
                self.guess_labels_list[i]['fg']= self.GUESS_FRAME_TEXT_AFTER
                button_text= current_guess_word.upper()
                if self.buttons[button_text[i]]['fg'] != "green":
                    self.buttons[button_text[i]]['fg'] = self.GUESS_FRAME_BG_WRONG 
                elif self.buttons[button_text[i]]['fg'] != "green":
                    self.buttons[button_text[i]]['fg'] = self.GUESS_FRAME_BG_WRONG 
                correct = 0  
                if self.word_guesslist[i] not in correct_word_lst:
                    self.letters_used_incorrect[i].append(self.word_guesslist[i])
        if hardmode_error == False and self.guess_frame_full == True:
            self.reset_values()
    
    def check_hardmode(self):
        """
        Checks if the input in hardmode can be used
        """
        self.correct_word = str(self.hidden_word.get())
        current_guess_word = ""
        correct_word_lst = []
        self.correct_word.lower()
        hardmode_error = False
        for i in range(len(self.correct_word)):
            correct_word_lst.append(self.correct_word[i])
        current_guess_word = ""
        correct_word_lst = []
        for i in range(len(self.correct_word)):
            correct_word_lst.append(self.correct_word[i])
        for i in range(len(self.word_guesslist)):
                current_guess_word += f"{self.word_guesslist[i]}"
                if self.word_guesslist[i] == self.correct_word[i]:
                    self.correct_letters[i].append(self.word_guesslist[i])
                if self.word_guesslist[i] in self.letters_used_yellow_flat:
                    self.letters_used_yellow_flat.remove(self.word_guesslist[i])
        #Check if the yellow letter was used correctly
        if len(self.letters_used_yellow_flat) > 0:
            self.display_error_message(f"{current_guess_word} is not consistent with previous guesses")
            hardmode_error = True
        current_guess_word = current_guess_word.lower()
        self.corr_wor_flat_list = reduce(operator.concat, self.correct_letters.values())
        for i in range(len(self.word_guesslist)):
            if self.word_guesslist[i] == correct_word_lst[i] and self.word_guesslist[i] in self.correct_letters[i]:
                #Turns in green if letterpass right and in right order
                pass
            elif self.word_guesslist[i] in correct_word_lst and self.word_guesslist[i] not in self.corr_wor_flat_list and self.word_guesslist[i] not in self.letters_used_yellow[i]:
                #Turns in orange if letter right but not right order
                pass
            elif self.word_guesslist[i] not in self.letters_used_incorrect_flat and len(self.correct_letters[i]) < 1 and self.word_guesslist[i] not in self.letters_used_yellow[i]:
                #Turns in grey if letter not right
                pass
            else:
                self.display_error_message(f"{current_guess_word} is not consistent with previous guesses")
                hardmode_error = True
                break
        if hardmode_error == False and self.guess_frame_full == True:
            self.change_colors_hardmode() #If there is no errors before changing colors

    def reset_values(self):
        """
        Clears values in guess_labels_list and word_guesslist.
        Adds 1 to row_squares
        Sets guess_frame_full equal to False
        """
        self.guess_labels_list.clear()
        self.row_squares +=1
        self.word_guesslist.clear()
        self.guess_frame_full = False
        self.letters_used_incorrect_flat = reduce(operator.concat, self.letters_used_incorrect.values())
        


    def back_button(self):
        """
        Destroys the current botton and moves to the back button
        """
        if self.column_squares >= 0 and self.game_over==False:
            self.guess_labels_list.pop()
            self.current_label.destroy()
            self.guess_frame_squares[self.row_squares][self.column_squares] = ""
            self.guess_frame_full = False
            self.word_guesslist = self.word_guesslist[:-1]
            if self.column_squares > 0:
                self.current_label = self.guess_labels_list[-1]
                self.column_squares -= 1        

    def show_hidden_word(self):
        """
        Shows and hides the word when the user clicks the show word checkmark
        """
        if self.showword_var.get():
            self.show_word_label.grid(row=3, column=2)
        else:
            self.show_word_label.grid_remove()

    def check_errors(self):
        """
        Check for errros before starting program
        """
        if self.specifyword_var.get() and self.guesses_var.get() == True:
            if len(self.entry_var.get()) == self.WORD_SIZE:
                if self.entry_var.get() in self.words_short:
                    self.hidden_word.set(str(self.entry.get()))
                    self.entry['state'] = 'disabled'
                    self.start_game()
                    #self.change_colors_squares1()
                #Checks for word in short list
                else:
                    self.display_error_message(f"{self.entry_var.get()} not in the word list")
            #Incorrect length
            elif self.start_button_bool == False:
                self.display_error_message("Incorrect specified word length")
     

        if self.specifyword_var.get() and self.guesses_var.get() == False:
            if len(self.entry_var.get()) == self.WORD_SIZE:
                self.hidden_word.set(str(self.entry.get()))
                self.entry['state'] = 'disabled'
                self.start_game()
            elif self.start_button_bool == False:
                self.display_error_message("Incorrect specified word length")

        elif self.guesses_var.get() and self.specifyword_var.get() == False:
            self.start_game()


    def display_error_message(self, error_message):
        """
        If error print the error message in display
        """
        self.error_message.set(error_message)
        self.error_label.grid(row=1, column=1)
        self.window.after(self.MESSAGE_DISPLAY_TIME_SECS*1000, self.hide_error_message)
    
    def hide_error_message(self):
        """
        After Indicated Time hide the message
        """
        self.error_label.grid_remove()

    def shortwordlist(self):
        """
        Creates a Python list containing a list of words whose length is self.WORD_SIZE
        from short_wordlist.txt 
        """
        try:
            f = open("short_wordlist.txt")
            for line in f:
                if len(line.strip())== self.WORD_SIZE:
                    self.words_short.append(line.strip())
        except FileNotFoundError:
            print("File Not Found")
        

    def longwordlist(self):
        """
        Creates a Python list containing a list of words whose length is self.WORD_SIZE
        from long_wordlist.txt 
        """
        try:
            f = open("long_wordlist.txt")
            for line in f:
                if len(line.strip()) == self.WORD_SIZE:
                    self.words_long.append(line.strip())
        except FileNotFoundError:
            print("File Not Found")

    def start_game(self):
        """
        Disables the checkbox and entry field.

        Prints out the state of the checkbox,
        and the contents of the entry field.
        """
        #Disable the check marks
        if self.start_button_bool == False:
            self.hardmode['state'] = 'disabled'
            self.guesses['state'] = 'disabled'
            self.specify_word['state'] = 'disabled'
            self.entry['state'] = 'disabled'
    
        if self.guesses_var.get() and self.specifyword_var.get() == False:
            self.hidden_word.set(random.choice(self.words_short))
            
        #Print Boolean Value of every variable
        print(f"Hard mode = {self.hardmode_var.get()}\n")
        print(f"Guesses must be words = {self.guesses_var.get()}\n")
        print(f"Show word = {self.showword_var.get()}\n")
        print(f"Specify word = {self.specifyword_var.get()}\n")
        print(f"Hidden word = {self.hidden_word.get()}\n")
        
        if self.specifyword_var.get():
            self.entry['state'] = 'normal'
            self.entry.delete(0, 'end')
            self.entry['state'] = 'disabled'

        #Checks if the game can start
        self.start_button_bool = True

    def quit(self):
        """
        Destroys the window
        """
        self.window.destroy()


if __name__ == "__main__":
   Wordy()