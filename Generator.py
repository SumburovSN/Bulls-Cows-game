"""
..module: Generator   - help to guess the riddled number
                    - the basis to play "Bools&Cows" with computer
..author: Sergey Sumburov <sumburovsn@gmail.com>
"""
# trialLog dictionary keeps all the responses of the current session of the game
# in form "attempt: response"
game_log = {
    '8134': 'B0 C1',
    # '9834': 'B0 C2',
    # '4297': 'B0 C1',
    # '7483': 'B1 C1',
    # '0152': 'B0 C2',
    # '0156': 'B0 C1',
    # '2507': 'B0 C1',
    # '1489': 'B0 C2',
    # '9320': 'B0 C2',
    # '7654': 'B1 C1'
}


# class Attempt for easy sorting the optimal request based on the amount of possible numbers
# to store them in list instead of dictionary
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
        function for sorting based on amount
        """
        return self.amount < other.amount


# function to get answer fo "Bulls&Cows" game
# @par: riddle and attempt both 4 symbols numeric
#
def compare(riddle, attempt):
    """
    compare function gets answer for "Bulls&Cows" game
    by comparison riddle to attempt
    :param riddle: the string consisted of 4 different numeric symbols to be recognised
    :param attempt: the string consisted of 4 different numeric symbols as an attempt to recognize the riddle
    :return result: the string of template 'B1 C2' ('B0 C0', 'B2 C2', etc.)
    """

    bulls = 0
    cows = 0

    # check every 4 symbols of the attempt against the riddle
    for i in range(4):
        if attempt[i] == riddle[i]:
            # if symbol is in the same position it contributes to bulls
            bulls += 1
        else:
            if attempt[i] in riddle:
                # if symbol is in the different position it contributes to cows
                cows += 1
    # the response of template 'B1 C2' ('B0 C0', 'B2 C2', etc.)
    return 'B' + str(bulls) + ' C' + str(cows)


def generate():
    """
    generate function returns the list of all possible numeric which correspond to the trialLog dictionary
    :return result: the list of all possible string of 4 numeric symbols
    """
    result = []
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
                    number = number0 + number1 + number2 + number3
                    is_correspond = True
                    for key in game_log.keys():
                        if compare(key, number) != game_log[key]:
                            is_correspond = False
                            break
                    if is_correspond:
                        result.append(number)
    return result


def generate_all():
    """
    generate function returns the list of all possible arrangements of 4 from 10 numeric symbols
    :return result: list of all possible arrangements of 4 from 10 numeric symbols
    """
    result = []
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
                    result.append(number0 + number1 + number2 + number3)
    return result


def analyze(whole, numeric):
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
    :param numeric: the list of all possible string of 4 numeric symbols from the generate function
    :return analysis: the dictionary of all possible answers and amounts of possible numeric for every entry
    """

    analysis = {}

    i = 0

    for head in whole:
        i += 1
        print("\r in progress... {:.0%}".format(i / 5040), end='')
        matrix = {}
        analysis[head] = matrix
        for current in numeric:
            result = compare(head, current)
            if result not in matrix:
                matrix[result] = 1
            else:
                matrix[result] += 1
    print(" Ready.")
    return analysis


def min_max(matrix):
    """
    min_max function forms the optimal request based on the minimum of all maximums values of Attempt class instances
    :param matrix: the dictionary from the analyze function
    :return result: the list of all possible string of 4 numeric symbols with minimum of all maximum
    """
    list_max = []
    result = []
    for key in matrix.keys():
        current = Attempt(key, 0)
        for value in matrix[key].values():
            if value > current.amount:
                current.amount = value
        list_max.append(current)

    list_max.sort()
    minimum = list_max[0].amount
    for attempt in list_max:
        if attempt.amount <= minimum:
            result.append(attempt)
    return result


output = generate()
if len(output) == 1:
    print("The riddle is {}".format(output[0]))
else:
    print("The amount of all the possible numbers: {}.".format(len(output)))
# print(10*9*8*7)
if input("Print the possible numbers ?(y/n)") == 'y':
    for element in output:
        print(element)

# result_matrix = analyze(output)
# if input("Print the matrix ?(y/n)") == 'y':
#     for element in result_matrix:
#         print(element + ":")
#         for response, amount in result_matrix[element].items():
#             print(response, amount)

# list_optimal = min_max(result_matrix)
# if input("Print the optimal list ?(y/n)") == 'y':
#     for response in list_optimal:
#         print(response.numeric, response.amount)

if input("Analyze against the whole set of arrangements?(y/n)") == 'y':
    result_matrix = analyze(generate_all(), output)
    list_optimal = min_max(result_matrix)
    priority = []
    for response in list_optimal:
        if response.numeric in output:
            priority.append(response)

    if priority:
        print("Priority length = {}".format(len(priority)))
        list_optimal = priority

    # if len(history_log) > 1:
    #     for response in list_optimal:


    if input("Print the all optimal list ?(y/n)") == 'y':
        for response in list_optimal:
            print(response.numeric, response.amount)
            for value, amount in result_matrix[response.numeric].items():
                print(value, amount)
