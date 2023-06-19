
import decimal
from decimal import Decimal

decimal.getcontext().prec = 100


class ArithmeticCoder:

    # source: https://www.youtube.com/watch?v=FdMoL3PzmSA
    # https://go-compression.github.io/algorithms/arithmetic/
    # constructor
    def __init__(self):
        self.all_char_counter = 0
        self.probability_table = {}
        self.freq_table = {}
        self.received_string = ""
        self.left_boundary = Decimal(0)
        self.right_boundary = Decimal(1)
        self.tag = (self.left_boundary + self.right_boundary)/2

    def coder_static(self, text, visualize=False, custom_prob={}):

        self.clean_cache()

        # update freq table
        for letter in text:
            if letter not in self.freq_table:
                self.freq_table[letter] = 1
            else:
                self.freq_table[letter] = self.freq_table[letter] + 1

        self.all_char_counter = len(text)
        self.received_string = text

        # if probability distribution is not provided, calculate it based on the appearance of letters in the string
        if len(custom_prob.keys()) == 0:

            # update prob table
            for letter in self.freq_table:
                self.probability_table[letter] = Decimal(self.freq_table[letter] / self.all_char_counter)

        else:
            self.probability_table = custom_prob

        # create boundaries
        # iterate through letters
        for j in range(0, len(self.received_string)):
            cumulative_boundary = {}
            temp_left_boundary = self.left_boundary
            # iterate through prob table to update boundaries
            for temp_char in self.probability_table.keys():
                prob_of_symbol = self.probability_table[temp_char]
                range_of_symbol = (self.right_boundary - self.left_boundary) * prob_of_symbol
                cumulative_boundary[temp_char] = {"left": temp_left_boundary,
                                                  "right": temp_left_boundary + range_of_symbol}
                temp_left_boundary = temp_left_boundary + range_of_symbol
            # update boundaries
            self.left_boundary = cumulative_boundary[self.received_string[j]]["left"]
            self.right_boundary = cumulative_boundary[self.received_string[j]]["right"]

            # update tag
            self.tag = (self.left_boundary + self.right_boundary)/2

            if visualize:
                print("left boundary: " + str(self.left_boundary))
                print("right boundary: " + str(self.right_boundary))
                print("encoded range: <" + str(self.left_boundary) + ", " + str(self.right_boundary) + ")")
                print("################################################")
                for _ in range(100):
                    print("-", end="")
                print("\n", end="")
                for key in self.freq_table.keys():
                    print("|", end="")
                    print(key * round((self.freq_table[key]/self.all_char_counter)*100), end="")
                    print("|", end="")
                print("\n", end="")
                for _ in range(100):
                    print("-", end="")
                print("\n", end="")
                print()

        if visualize:
            print("frequency table: " + str(self.freq_table))
            print("probability table:" + str(self.probability_table))
            print("received string: " + self.received_string)

        return "<" + str(self.left_boundary) + ", " + str(self.right_boundary) + ")"

    # clear cached info
    def clean_cache(self):
        self.all_char_counter = 0
        self.probability_table = {}
        self.freq_table = {}
        self.received_string = ""
        self.left_boundary = 0
        self.right_boundary = 1
