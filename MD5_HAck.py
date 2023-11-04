from hashlib import md5
import itertools
import string

def guess_password(real):
    chars = string.ascii_lowercase
    attempts = 0
    for password_length in range(1, 15):
        for guess in itertools.product(chars, repeat=password_length):
            attempts += 1
            guess = ''.join(guess)
            if guess == real:
                return 'password is {}. found in {} guesses.'.format(guess, attempts)
            # uncomment to display attempts, though will be slower
            if attempts % 10000 == 0:
                print(guess, attempts)
    return 'password is {}. not found in {} guesses.'.format(guess, attempts)

print(guess_password('admin'))