import string
import random


def symbols_generator(n, only_letters=True):
    # returns only letters
    if only_letters:
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))
    # returns letters and digits
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


def bits_generator(n):
    return ''.join(str(random.randint(0, 1)) for _ in range(n))
