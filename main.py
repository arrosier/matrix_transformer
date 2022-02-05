import numpy as np

from matrix_transformer import transformer


KEYBOARD_ARRAY = np.array([
        ['1','2','3','4','5','6','7','8','9','0'],
        ['Q','W','E','R','T','Y','U','I','O','P'],
        ['A','S','D','F','G','H','J','K','L',';'],
        ['Z','X','C','V','B','N','M',',','.','/']
        ])
CIPHER = "S1"
INPUT = "DOG"


if __name__ == "__main__":
    enciphered_text = transformer.execute(KEYBOARD_ARRAY, CIPHER, INPUT)
    print(enciphered_text)
