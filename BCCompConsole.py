"""
Copyright 2018 by Sergey Sumburov <sumburovsn@gmail.com>
All rights reserved.
This file is part of the Bulls&Cows game package,
and is released under the "MIT License Agreement". Please see the LICENSE
file that should have been included as part of this package.
"""

import BullsCows


def game():
    bulls_cows = BullsCows.CompGame()
    print("The game has been started.\n "
          "Type the response in the form 'Bx Cy' where x - bulls amount , y - cows amount.\n "
          "Print 'exit' for exit")

    while not bulls_cows.isFinished:
        request = bulls_cows.suggest()
        if request == '0':
            print("One of your responses was wrong.\n Let's start new game.")
            return

        if len(bulls_cows.rest) == 1:
            print("{}. The riddle is {}".format(len(bulls_cows.game_log)+1, request))
            return

        print("{}. Attempt: {}".format(len(bulls_cows.game_log)+1, request))

        while True:
            response = input("Your response: ")

            if response == 'exit':
                print("The game is over...")
                bulls_cows.isFinished = True
                return
            try:
                bulls_cows.check(response)
                break
            except TypeError as error:
                print(error)

        bulls_cows.game_log.update({request: response})


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
