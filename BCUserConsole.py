"""
Copyright 2018 by Sergey Sumburov <sumburovsn@gmail.com>
All rights reserved.
This file is part of the Bulls&Cows game package,
and is released under the "MIT License Agreement". Please see the LICENSE
file that should have been included as part of this package.
"""

import BullsCows


def game():
    bulls_cows = BullsCows.UserGame()

    while True:
        trial = input("Print 4 different numbers: ")

        if trial == 'exit':
            print("The number was " + bulls_cows.puzzle + ".")
            print("The game is over...")
            return

        try:
            bulls_cows.check(trial)
        except TypeError as error:
            print(error)
            continue

        result = bulls_cows.compare(bulls_cows.puzzle, trial)
        bulls_cows.game_log.update({trial: result})
        print(trial + ' ' + bulls_cows.game_log[trial])
        if result == 'B4 C0':
            print(f"You've guessed in {len(bulls_cows.game_log)} move(s)")
            return


"""
================================================================================================
>>> main
This section is the 'main' or starting point of the Bulls&Cows program. 
The python interpreter will find this 'main' routine and execute it first.
================================================================================================       
"""

if __name__ == '__main__':
    while input("Do you want play Bulls&Cows (y/n)?") not in ('n', 'N', 'No'):
        game()
