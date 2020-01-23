"""
Copyright 2018 by Sergey Sumburov <sumburovsn@gmail.com>
All rights reserved.
This file is part of the Bulls&Cows game package,
and is released under the "MIT License Agreement". Please see the LICENSE
file that should have been included as part of this package.
"""

import random


class BullsCows:
    """
    class BullsCows is interface wrapper and contains functions for 2 subclasses:
    UserGuess and CompGuess
    """

    @staticmethod
    def pick():
        numeric = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        puzzle = ''

        while len(puzzle) != 4:
            var = int(random.random()*10)
            if var in numeric:
                puzzle += str(var)
                numeric.remove(var)

        return puzzle

    @staticmethod
    def compare(riddle, attempt):
        bulls = 0
        cows = 0

        for i in range(4):
            if attempt[i] == riddle[i]:
                bulls += 1
            else:
                if attempt[i] in riddle:
                    cows += 1

        return 'B' + str(bulls) + ' C' + str(cows)


class UserGame(BullsCows):
    def __init__(self):
        self.game_log = {}
        self.puzzle = BullsCows.pick()

    def check(self, attempt):
        trial = ""

        if len(attempt) != 4:
            raise TypeError("Symbols != 4.")

        for i in range(4):
            if attempt[i] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                raise TypeError("Symbols must be numeric.")
            if attempt[i] not in trial:
                trial += attempt[i]
            else:
                raise TypeError("Symbols must be different.")

        if trial in self.game_log.keys():
            raise TypeError("The number has been checked already.")

        return trial


class CompGame(BullsCows):
    def __init__(self):
        self.game_log = {}
        self.isFinished = False
        self.full = CompGame.generate_full()
        self.rest = self.full.copy()

    @staticmethod
    def check(attempt):
        right = ['B4 C0', 'B3 C0',
                 'B2 C2', 'B2 C1', 'B2 C0',
                 'B1 C3', 'B1 C2', 'B1 C1', 'B1 C0',
                 'B0 C4', 'B0 C3', 'B0 C2', 'B0 C1', 'B0 C0']

        if attempt not in right:
            raise TypeError("Wrong input.")
        else:
            result = attempt

        return result

    @staticmethod
    def generate_full():
        """
        generate function returns the list of all possible arrangements of 4 from 10 numeric symbols
        :return full: list of all possible arrangements of 4 from 10 numeric symbols
        """
        full = []
        numeric0 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for number0 in numeric0:
            numeric1 = numeric0.copy()
            numeric1.remove(number0)
            for number1 in numeric1:
                numeric2 = numeric1.copy()
                numeric2.remove(number1)
                for number2 in numeric2:
                    numeric3 = numeric2.copy()
                    numeric3.remove(number2)
                    for number3 in numeric3:
                        full.append(number0 + number1 + number2 + number3)
        return full

    class Attempt:
        """
        class Attempt for easy sorting the optimal request based on the amount of possible numbers
        to store them in list instead of dictionary
        """

        def __init__(self, numeric, amount):
            """
            function to make an instance of Attempt
            """
            self.numeric = numeric
            self.amount = amount

        def __lt__(self, other):
            """
            override function for sorting based on amount
            """
            return self.amount < other.amount

    def generate_rest(self):
        """
        generate function returns the list of all possible numeric which correspond to the trialLog dictionary
        :return result: the list of all possible string of 4 numeric symbols
        """
        new = []
        key = list(self.game_log.keys())[-1]
        for number in self.rest:
            if self.compare(key, number) == self.game_log[key]:
                new.append(number)

        self.rest = new

    def analyze(self, widget=None):
    # def analyze(self):
        """
        analyze function returns the dictionary of the form, e.g.:
        {'1234':    {'B0 C1': 14,
                    'B1 C1': 3}
        '5678':     {'B1 C2': 1,
                    'B2 C0': 30}
        ...
        }
        for each numeric it contains the dictionary of the possible responses and corresponding them amounts of possible
        numeric
        :return analysis: the dictionary of all possible answers and amounts of possible numeric for every entry
        """

        analysis = {}

        i = 0
        if widget:
            widget['value'] = i
            widget['maximum'] = 5040
        for head in self.full:
            i += 1
            if widget:
                widget['value'] = i
                widget.master.update()
            print("\r in progress... {:.0%}".format(i / 5040), end='')

            matrix = {}
            analysis[head] = matrix
            for current in self.rest:
                result = BullsCows.compare(head, current)
                if result not in matrix:
                    matrix[result] = 1
                else:
                    matrix[result] += 1
        print(" Ready.")
        return analysis

    @staticmethod
    def min_max(analysis):
        """
        min_max function forms the optimal request based on the minimum of all maximums values of Attempt class instances
        :param analysis: the dictionary from the analyze function
        :return result: the list of all possible string of 4 numeric symbols with minimum of all maximum
        """
        list_max = []
        result = []
        for key in analysis.keys():
            current = CompGame.Attempt(key, 0)
            for value in analysis[key].values():
                if value > current.amount:
                    current.amount = value
            list_max.append(current)

        list_max.sort()
        minimum = list_max[0].amount
        for attempt in list_max:
            if attempt.amount <= minimum:
                result.append(attempt)
        return result

    def suggest(self, widget=None):

        if len(self.game_log) == 0:
            trial = BullsCows.pick()
        else:
            self.generate_rest()

            if len(self.rest) == 0:
                trial = "0"
                self.isFinished = True
            else:
                if len(self.rest) == 1:
                    trial = self.rest[0]
                    self.isFinished = True
                else:
                    analysis = self.analyze(widget)
                    list_optimal = CompGame.min_max(analysis)
                    priority = []
                    for response in list_optimal:
                        if response.numeric in self.rest:
                            priority.append(response)

                    if priority:
                        list_optimal = priority

                    index = int(random.random() * len(list_optimal))
                    trial = list_optimal[index].numeric

        return trial
