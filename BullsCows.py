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
        """
        function picks up a random 4-digit string to guess by user
        :return puzzle: 4-digit string to guess by user
        """
        numeric = '0123456789'

        puzzle = ''

        while len(puzzle) != 4:
            var = numeric[int(random.random()*len(numeric))]
            puzzle += var
            numeric = numeric.replace(var, '')

        return puzzle

    @staticmethod
    def compare(puzzle, attempt):
        """
        function compares two 4-digit strings namely puzzle (or number to guess by user) and attempt (input by user)
        :return result in form "Bx Cy" where x - number of bulls and y - number of cows
        """
        bulls = 0
        cows = 0

        for i in range(4):
            if attempt[i] == puzzle[i]:
                bulls += 1
            else:
                if attempt[i] in puzzle:
                    cows += 1

        return 'B' + str(bulls) + ' C' + str(cows)


class UserGame(BullsCows):
    """
    class provides an interface for the game where a user tries to figure out the puzzle picked up by a computer
    game_log keeps the history of requests and responses in the form:
    game_log = {
    '8134': 'B0 C1',
    9834': 'B0 C2',
    ...
    }
    User game started with picking up the puzzle
    """
    def __init__(self):
        self.game_log = {}
        self.puzzle = BullsCows.pick()

    def check(self, attempt):
        """
        function handles with user inputs. It handles the next wrong inputs:
        - wrong number of symbols;
        - wrong symbols;
        - same symbols in the request;
        - the request is already in game_log (the user already input that request earlier in the game session)
        :return request
        """
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
        # self.isFinished = False
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
        :return full: list of all possible arrangements of 4 from 10 numeric symbols with length 5040
        """
        full = []
        numeric0 = '0123456789'
        for number0 in numeric0:
            numeric1 = numeric0.replace(number0, '')
            for number1 in numeric1:
                numeric2 = numeric1.replace(number1, '')
                for number2 in numeric2:
                    numeric3 = numeric2.replace(number2, '')
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
        generate function returns the list of all possible numeric which correspond to the game_log dictionary
        :return result: the list of all possible string of 4 numeric symbols
        """
        rest_new = []
        key = list(self.game_log.keys())[-1]
        for number in self.rest:
            if self.compare(key, number) == self.game_log[key]:
                rest_new.append(number)

        self.rest = rest_new


    def analyze(self, widget=None):
        """
        analyze function returns the array of the entries each of them is also array, e.g.:
        [
        ['1234', 338], <- the entry
        ...
        ['5678', 234]],
        ...
        ]
        Each numeric of full array is checked against each numeric in rest array, then results are aggregated according their combinations ('B0 C1', 'B0 C2', etc.),
        and maximum of all possible combinations is chosen to put into entry array.
        :return analysis: the array of all possible numeric and maximum amount of possible responses for every entry.
        """

        analysis = []

        i = 0
        if widget:
            widget['value'] = i
            widget['maximum'] = 5040
        for head in self.full:
            i += 1
            if widget:
                widget['value'] = i
                widget.master.update()

            # it prints in one row in PyCharm, not in IDLE
            print("\r in progress... {:.0%}".format(i / 5040), end='')

            amounts = []
            responses = []

            for current in self.rest:
                result = BullsCows.compare(current, head)
                try:
                    index = responses.index(result)
                except:
                    index = -1
                if index >= 0:
                    amounts[index] += 1
                else:
                    responses.append(result)
                    amounts.append(1)
            amounts.sort(reverse=True)
            analysis.append(CompGame.Attempt(head, amounts[0]))

        print(" Ready.")
        return analysis

    @staticmethod
    def min_max(analysis):
        """
        minFromMax function forms the optimal request based on the minimum of all maximums values
        requires protection against empty rest array
        :param analysis: the array from the analyze function
        :return result: the array of all possible string of 4 numeric symbols with minimum of all maximum
        """

        result = []
        analysis.sort()

        minimum = analysis[0].amount
        i = 0
        while analysis[i].amount == minimum:
            result.append(analysis[i].numeric)
            i += 1

        return result

    def suggest(self, widget=None):
        """
        suggest function get the next request for User to be checked
        requires protection against empty rest array
        The sequence is below:
        1. If game started, pick up random number;
        2. Check if rest array is empty => one of responses was wrong, terminate the game;
        3. if rest array contains 1 number => it's the riddle;
        4. Make the optimal list and pick up the random number from it.
        :return trial: the next request of possible string of 4 numeric symbols
        :param widget: reference to progress bar
        :return trial: the next request of possible string of 4 numeric symbols
        """
        if len(self.game_log) == 0:
            trial = BullsCows.pick()
        else:
            self.generate_rest()

            if len(self.rest) == 0:
                trial = "0"

            else:
                if len(self.rest) == 1:
                    trial = self.rest[0]

                else:
                    analysis = self.analyze(widget)
                    list_optimal = CompGame.min_max(analysis)
                    priority = []
                    for response in list_optimal:
                        if response in self.rest:
                            priority.append(response)

                    if priority:
                        list_optimal = priority

                    index = int(random.random() * len(list_optimal))
                    trial = list_optimal[index]

        return trial
