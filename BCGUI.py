"""
Copyright 2018 by Sergey Sumburov <sumburovsn@gmail.com>
All rights reserved.
This file is part of the Bulls&Cows game package,
and is released under the "MIT License Agreement". Please see the LICENSE
file that should have been included as part of this package.
"""

import BullsCows
import Rules
import License
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk


class Game(Frame):
    def __init__(self):
        self.userGuess = ""
        self.compGuess = ""
        self.request = ""
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Bulls&Cows")

        self.user_panel = PanedWindow(self, orient=VERTICAL)
        self.user_panel.grid(row=0, column=0, columnspan=2, sticky=W + E + N + S)
        self.user_label = Label(self.user_panel, text="User guessing game", fg="blue")
        self.user_label.grid(row=0, column=0, columnspan=2, sticky=W + E + N + S)
        self.input_label = Label(self.user_panel, text="Input 4 different numbers: ", fg="blue")
        self.input_label.grid(row=1, column=0, columnspan=1, sticky=W + E + N + S)
        self.input_entry = Entry(self.user_panel, bd=3)
        self.input_entry.grid(row=1, column=1, columnspan=1, sticky=W + E + N + S)
        self.check_button = Button(self.user_panel, text="Check input (Enter)", width=25, command=self.check, fg="blue")
        self.check_button.grid(row=2, column=0, columnspan=1, sticky=W + E + N + S)
        self.user_game_button = Button(self.user_panel, text="New game (F2)", width=25, command=self.user_game,
                                       fg="blue")
        self.user_game_button.grid(row=3, column=0, columnspan=1, sticky=S + W + E + N)

        self.text = Text(self, width=50)
        self.text.insert(END, "Push 'New game'.")
        self.text.grid(row=0, column=2, columnspan=1, sticky=W + E + N + S)
        self.text.tag_config("user", foreground="blue")
        self.text.tag_config("alarm", foreground="red")
        self.text.tag_config("comp", foreground="green")

        self.comp_panel = PanedWindow(self, orient=VERTICAL)
        self.comp_panel.grid(row=0, column=3, columnspan=2, sticky=W + E + N + S)
        self.comp_label = Label(self.comp_panel, text="Computer guessing game", fg="green")
        self.comp_label.grid(row=0, column=0, columnspan=2, sticky=W + E + N + S)
        self.bulls_label = Label(self.comp_panel, text="Bulls: ", fg="green")
        self.bulls_label.grid(row=1, column=0, columnspan=1, sticky=W + E + N + S)
        self.bulls_entry = Entry(self.comp_panel, bd=3)
        self.bulls_entry.grid(row=1, column=1, columnspan=1, sticky=W + E + N + S)
        self.cows_label = Label(self.comp_panel, text="Cows: ", fg="green")
        self.cows_label.grid(row=2, column=0, columnspan=1, sticky=W + E + N + S)
        self.cows_entry = Entry(self.comp_panel, bd=3)
        self.cows_entry.grid(row=2, column=1, columnspan=1, sticky=W + E + N + S)
        self.input_button = Button(self.comp_panel, text="Input results (Ctrl-Enter)", width=25, command=self.input,
                                   fg="green")
        self.input_button.grid(row=3, column=0, columnspan=1, sticky=W + E + N + S)
        self.comp_game_button = Button(self.comp_panel, text="New game (Ctrl-F2)", width=25, command=self.comp_game,
                                       fg="green")
        self.comp_game_button.grid(row=4, column=0, columnspan=1, sticky=S + W + E + N)
        self.bar = ttk.Progressbar(self.comp_panel, mode="determinate")
        self.bar.grid(row=5, column=0, columnspan=2, sticky=S + W + E + N)

        self.menu_bar = Menu(self)
        self.master.config(menu=self.menu_bar)
        self.game_menu = Menu(self.menu_bar, tearoff=0)
        self.game_menu.add_command(label="New User guessing game (F2)", command=self.user_game)
        self.game_menu.add_command(label="New Computer guessing game (Ctrl-F2)", command=self.comp_game)
        self.game_menu.add_command(label="Exit", command=self.master.destroy)
        self.menu_bar.add_cascade(label="Game", menu=self.game_menu)
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.about)
        self.help_menu.add_command(label="Game rules (F1)", command=self.rules)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.master.bind("<Return>", self.check)
        self.master.bind("<F2>", self.user_game)
        self.master.bind("<Control - Return>", self.input)
        self.master.bind("<Control - F2>", self.comp_game)

        self.master.bind("<F1>", self.rules)

    def user_game(self, event=None):
        if self.userGuess:
            self.text.insert(END, "\nThe game is over. The puzzle was {}.".format(self.userGuess.puzzle))
            self.text.tag_add("user", "end -1 lines", "end-1c")
            self.userGuess = ""

        self.userGuess = BullsCows.UserGame()
        self.text.insert(END, "\nThe User guessing game has been started.")
        self.text.tag_add("user", "end -1 lines", "end-1c")
        self.text.see(END)
        self.input_entry.focus()

    def check(self, event=None):
        if not self.userGuess:
            self.text.insert(END, "\nPush 'New game'.")
            self.text.tag_add("alarm", "end -1 lines", "end-1c")
            self.text.see(END)
            return
        trial = self.input_entry.get()
        try:
            self.userGuess.check(trial)
            result = self.userGuess.compare(self.userGuess.puzzle, trial)
            self.userGuess.game_log.update({trial: result})
            self.text.insert(END, "\n{}. {} {}".format(len(self.userGuess.game_log), trial,
                                                       self.userGuess.game_log[trial]))
            self.text.tag_add("user", "end -1 lines", "end-1c")
            self.text.see(END)
            self.input_entry.delete(0, 4)
            if result == 'B4 C0':
                self.text.insert(END, "\nYou've guessed in {} move(s).".format(len(self.userGuess.game_log)))
                self.text.tag_add("user", "end -1 lines", "end-1c")
                self.text.see(END)
                self.userGuess = ""
                return
        except TypeError as error:
            self.text.insert(END, "\n{}".format(error))
            self.text.tag_add("alarm", "end -1 lines", "end-1c")
            self.text.see(END)

    def comp_game(self, event=None):
        self.text.insert(END, "\nThe Computer guessing game has been started.")
        self.text.tag_add("comp", "end -1 lines", "end-1c")
        self.compGuess = BullsCows.CompGame()
        self.request = self.compGuess.suggest(self.bar)
        self.text.insert(END, "\n{}. Attempt: {}".format(len(self.compGuess.game_log) + 1, self.request))
        self.text.tag_add("comp", "end -1 lines", "end-1c")
        self.text.see(END)
        self.bulls_entry.focus()

    def input(self, event=None):
        if not self.compGuess:
            self.text.insert(END, "\nPush 'New game'")
            self.text.tag_add("alarm", "end -1 lines", "end-1c")
            self.text.see(END)
            return

        response = "B" + self.bulls_entry.get() + " " + "C" + self.cows_entry.get()

        try:
            self.compGuess.check(response)
        except TypeError as error:
            self.text.insert(END, "\n{}".format(error))
            self.text.tag_add("alarm", "end -2 lines", "end-1c")
            self.text.see(END)
            return

        self.compGuess.game_log.update({self.request: response})

        self.bar.start()
        self.request = self.compGuess.suggest(self.bar)
        self.bar.stop()

        if self.request == '0':
            self.text.insert(END, "\nOne of your responses was wrong.\n Let's start new game.")
            self.text.tag_add("comp", "end -2 lines", "end-1c")
            self.compGuess = ""
            return

        if len(self.compGuess.rest) == 1:
            self.text.insert(END, "\n{}. The riddle is {}".format(len(self.compGuess.game_log) + 1, self.request))
            self.text.tag_add("comp", "end -1 lines", "end-1c")
            self.compGuess = ""
            return

        self.text.insert(END, "\n{}. Attempt: {}".format(len(self.compGuess.game_log) + 1, self.request))
        self.text.tag_add("comp", "end -1 lines", "end-1c")
        self.text.see(END)
        self.bulls_entry.focus()

    @staticmethod
    def rules(event=None):
        rules = Rules.rules
        messagebox.showinfo("Game rules", rules)

    @staticmethod
    def about(event=None):
        info = License.license
        messagebox.showinfo("About", info)


def main():
    Game().mainloop()


"""
================================================================================================
>>> main
This section is the 'main' or starting point of the Bulls&Cows program. 
The python interpreter will find this 'main' routine and execute it first.
================================================================================================       
"""
if __name__ == '__main__':
    main()
