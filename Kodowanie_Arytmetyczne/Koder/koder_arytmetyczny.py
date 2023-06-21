import decimal
from decimal import Decimal

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
        decimal.getcontext().prec = 100

    def coder_static(self, text, visualize=False, custom_prob={}):

        assert len(text) <= 82, "Provided text is too long"

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

    # decoding, r- chosen value between boundaries
    def dekoder_static(self, r):

        # local variables
        process_left_boundary = Decimal(0)
        process_right_boundary = Decimal(1)
        cumulative_boundary = {}
        string_to_return = ""
        r = Decimal(r)

        # check if value is valid
        assert self.left_boundary <= r < self.right_boundary, "r should be between left and right boundary (inclusive)"

        # check if the probability table was provided
        assert len(self.probability_table) != 0, "probability table was not provided"

        # process data
        while 1:
            temp_left_boundary = process_left_boundary

            # update cumulative boundaries
            for temp_char in self.probability_table.keys():
                prob_of_symbol = self.probability_table[temp_char]
                range_of_symbol = (process_right_boundary - process_left_boundary) * prob_of_symbol
                cumulative_boundary[temp_char] = {"left": temp_left_boundary,
                                                  "right": temp_left_boundary + range_of_symbol}
                temp_left_boundary = temp_left_boundary + range_of_symbol

                if cumulative_boundary[temp_char]["left"] < r < cumulative_boundary[temp_char]["right"]:
                    string_to_return = string_to_return + temp_char
                    process_left_boundary = cumulative_boundary[temp_char]["left"]
                    process_right_boundary = cumulative_boundary[temp_char]["right"]
                    break

            # end if boundaries were meet
            if self.left_boundary.compare(process_left_boundary) == 0 and \
                    self.right_boundary.compare(process_right_boundary) == 0:
                break

        return "Decoded string: " + string_to_return
