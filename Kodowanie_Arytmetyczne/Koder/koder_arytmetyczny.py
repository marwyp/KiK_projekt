import decimal
from decimal import Decimal
import sys


class ArithmeticCoder:

    # source: https://www.youtube.com/watch?v=FdMoL3PzmSA
    # https://go-compression.github.io/algorithms/arithmetic/
    # constructor
    def __init__(self):
        self.PROB_PREC = 80
        self.COMP_PREC = 8000
        decimal.getcontext().prec = self.COMP_PREC
        self.all_char_counter = 0
        self.probability_table = {}
        self.freq_table = {}
        self.received_string = ""
        self.left_boundary = Decimal("0")
        self.right_boundary = Decimal("1")
        self.tag = (self.left_boundary + self.right_boundary) / Decimal("2")

    def coder_static(self, text, visualize=False, custom_prob={}):

        # clear from previous coding
        if self.all_char_counter != 0:
            self.clean_cache()

        # print log
        print("Starting to code received string...")

        # log
        print("Initialize probability and frequency tables...")

        # create freq table
        for letter in text:
            if letter not in self.freq_table:
                self.freq_table[letter] = 1
            else:
                self.freq_table[letter] = self.freq_table[letter] + 1

        self.all_char_counter = len(text)
        self.received_string = text

        # if probability distribution is not provided, calculate it, based on the appearance of letters in the string
        if len(custom_prob.keys()) == 0:
            self.create_probabilty_table()
        else:
            self.probability_table = custom_prob

        # log
        print("Coding...")

        # create boundaries; iterate through letters
        for j in range(0, len(self.received_string)):

            # print progres
            print("\r" + "Words encoded: " + str(j+1) + "/" + str(self.all_char_counter), end='', flush=True)

            cumulative_boundary = {}
            temp_left_boundary = self.left_boundary
            # iterate through prob table to update boundaries
            for temp_char in self.probability_table.keys():
                prob_of_symbol = self.probability_table[temp_char]
                range_of_symbol = Decimal(self.right_boundary - self.left_boundary).fma(prob_of_symbol, 0)
                cumulative_boundary[temp_char] = {"left": temp_left_boundary,
                                                  "right": temp_left_boundary + range_of_symbol}
                temp_left_boundary = temp_left_boundary + range_of_symbol
            # update boundaries
            self.left_boundary = cumulative_boundary[self.received_string[j]]["left"]
            self.right_boundary = cumulative_boundary[self.received_string[j]]["right"]

            # optimize
            temp = self.__optimize(self.left_boundary, self.right_boundary)
            if temp:
                self.left_boundary = Decimal(temp[0])
                self.right_boundary = Decimal(temp[1])
            # update tag
            self.tag = (self.left_boundary + self.right_boundary) / Decimal("2")

        print()
        if visualize:
            print("frequency table: " + str(self.freq_table))
            print("probability table:" + str(self.probability_table))
            print("left boundary: " + str(self.left_boundary))
            print("right boundary: " + str(self.right_boundary))
            print("encoded range: <" + str(self.left_boundary) + ", " + str(self.right_boundary) + ")")
            print("received string: " + self.received_string)
        # end log
        print("Encoding finished.")
        print("precision: " + str(len(str(self.tag.normalize())) - 2))
        return self.tag.normalize()

    # adjust probability table in a such way, that it would resemble Gaussian distribution
    def create_probabilty_table(self):
        decimal.getcontext().prec = self.PROB_PREC
        # create prob table
        for letter in self.freq_table:
            self.probability_table[letter] = (Decimal(str(self.freq_table[letter])) /
                                              Decimal(str(self.all_char_counter))).normalize()
        decimal.getcontext().prec = self.COMP_PREC

    # find the nearest different digit in Decimal
    def __optimize(self, left, right):

        # cast to string
        left_string = str(Decimal(left).normalize())
        right_string = str(Decimal(right).normalize())
        # change to the non-exponential notation
        if "E" in left_string:
            indicator = left_string.find("E")
            multi = int(left_string[indicator + 2:])
            left_string = "0." + ("0" * multi) + left_string[2: indicator]

        if "E" in right_string:
            indicator = right_string.find("E")
            multi = int(right_string[indicator + 2:])
            right_string = "0." + ("0" * multi) + right_string[2: indicator]
        # find the very first place on which two floats are different
        precision = min(len(left_string), len(right_string))
        if precision >= 2:
            for i in range(0, precision):
                # skip for '.'
                if left_string[i] == "." or right_string[i] == ".":
                    continue
                # take only those digit that are the same and 3 after that are different
                if int(left_string[i]) != int(right_string[i]):
                    left_string = left_string[0:i+5]
                    right_string = right_string[0:i+5]
                    break
            return [left_string, right_string]

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
        process_left_boundary = Decimal("0")
        process_right_boundary = Decimal("1")
        string_to_return = ""
        r = Decimal(str(r))
        iteration = 1

        # start log
        print("Starting to decoded...")

        # check if value is valid
        assert self.left_boundary <= r < self.right_boundary, "r should be between left and right boundary (inclusive)"

        # check if the probability table was provided
        assert len(self.probability_table) != 0, "probability table was not provided"

        # process data
        while 1:
            # print progres
            print("\r" + "Words decoded: " + str(iteration) + "/" + str(self.all_char_counter), end='', flush=True)
            # local variables
            temp_left_boundary = process_left_boundary
            cumulative_boundary = {}

            # update cumulative boundaries
            for temp_char in self.probability_table.keys():
                prob_of_symbol = self.probability_table[temp_char]
                range_of_symbol = Decimal(process_right_boundary - process_left_boundary).fma(prob_of_symbol, 0)
                cumulative_boundary[temp_char] = {"left": temp_left_boundary,
                                                  "right": temp_left_boundary + range_of_symbol}
                temp_left_boundary = temp_left_boundary + range_of_symbol
                if r.compare(cumulative_boundary[temp_char]["left"]) == 1 and \
                        r.compare(cumulative_boundary[temp_char]["right"]) == -1:
                    string_to_return = string_to_return + temp_char
                    iteration += 1
                    process_left_boundary = cumulative_boundary[temp_char]["left"]
                    process_right_boundary = cumulative_boundary[temp_char]["right"]
                    break

            # optimize
            temp = self.__optimize(process_left_boundary, process_right_boundary)
            if temp:
                process_left_boundary = Decimal(temp[0])
                process_right_boundary = Decimal(temp[1])

            # end if boundaries were meet
            if self.left_boundary.compare(process_left_boundary) == 0 and \
                    self.right_boundary.compare(process_right_boundary) == 0:
                break
        print()
        # end log
        print("Decoding finished.")
        return "Decoded string: " + string_to_return
