import numpy as np

from . import operations, validation, constants


def execute(keyboard_array: np.ndarray, cipher: str, input: str) -> str:
    """
    Validate the cipher and input string then perform the transformation and return the output string.

    Arguments:
    keyboard_array: The original keyboard array
    cipher: The cipher to validate
    input: The input string to validate

    Returns:
    The input string 'retyped' on the transformed matrix.
    """

    validation.validate_cipher(cipher)
    validation.validate_input_string(keyboard_array, input)
    new_matrix = _transform(keyboard_array, cipher)
    return _get_output(keyboard_array, new_matrix, input)


def _transform(matrix: np.ndarray, cipher: str) -> np.ndarray:
    """
    Perform defined matrix operations on a provided matrix based on a given set of instructions.

    Arguments:
    matrix: The matrix upon which the operators should be applied
    cipher: A string of characters (and supported symbols) that represent a specified operator.

    Returns:
    The input matrix after all transformations have been applied.
    """

    # Since the keyboard matrix that we are operating on is relatively small a quick copy here isn't too expensive; however, if this were to change to something a little meatier
    # in the future we probably don't want to do this.
    output = matrix.copy()
    last_index = len(cipher) - 1
    for index,char in enumerate(cipher):
        if char == constants.HORIZONTAL_FLIP:
            output = operations.horizontal_flip(output)
        elif char == constants.VERTICAL_FLIP:
            output = operations.vertical_flip(output)
        elif char == constants.SHIFT:
            output = operations.shift(output, cipher, index + 1, last_index)
        else:
            # Prior to this step we've already validated the cipher so any remaining characters not covered here are valid but don't require an operation (e.g. numbers, etc)
            continue

    return output

def _get_output(keyboard_array: np.ndarray, matrix: np.ndarray, input: str) -> str:
    """
    Return the re-typed string using the transformed matrix based on the coordinates of the original keyboard.

    Arguments:
    keyboard_array: The original keyboard array
    matrix: The transformed keyboard array
    input: The input string to print

    Returns:
    The input string 'retyped' on the transformed matrix.
    """

    output = "".join(matrix[keyboard_array == char][0] for char in input)
    return output
