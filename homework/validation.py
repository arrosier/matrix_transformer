import numpy as np

from . import constants


VALID_CIPHER_CHARACTERS = [constants.HORIZONTAL_FLIP,constants.VERTICAL_FLIP,constants.SHIFT,'-','0','1','2','3','4','5','6','7','8','9']

def validate_cipher(cipher: str) -> None:
    """Validate the cipher."""

    validate_legal_characters(cipher)
    validate_shift_operator(cipher)
    validate_miscellaneous_characters(cipher)

def validate_legal_characters(cipher: str) -> None:
    """Verify the cipher is not empty and all characters in the cipher are valid."""

    if not cipher:
        raise ValueError("Cipher cannot be empty.")

    for index,value in enumerate(cipher):
        if value not in VALID_CIPHER_CHARACTERS:
            raise ValueError("Unsupported cipher character found at position %d." % index)

def validate_shift_operator(cipher: str) -> None:
    """Verify any shift operator in the cipher can be parsed correctly."""

    shift_indices = _find_indices_of_char(cipher, constants.SHIFT)
    for index in shift_indices:
        # A shift operator should always be followed immediately by a number or a negative sign.
        if not (cipher[index + 1].isdigit() or cipher[index + 1] == '-'):
            raise ValueError("Invalid shift operator found at position %d. A shift operator should always be followed by either a number or a negative sign." % index)

def validate_miscellaneous_characters(cipher: str) -> None:
    """Verify all valid, non-operator characters are correctly located in the cipher."""

    negative_sign_indices = _find_indices_of_char(cipher, '-')
    last_index = len(cipher) - 1
    # A negative sign should never be the first or last character in the cipher.
    if (cipher[0] == '-' or cipher[last_index] == '-'):
        raise ValueError("Negative sign found at the first or last position of the cipher. Please update and try again.")

    for index in negative_sign_indices:
        # A negative sign should only appear immediately before a number.
        if not cipher[index + 1].isdigit():
            raise ValueError("Invalid negative sign found in the cipher at position %d. A negative sign should only appear immediately before a number." % index)

def validate_input_string(keyboard_array: np.ndarray, input: str) -> None:
    """Verify that all characters in the input string can be matched to the provided keyboard array."""

    if not input:
        raise ValueError("Input cannot be empty.")
    
    # The incoming keyboard array acts as our VALID_CIPHER_CHARACTERS analog since we'll be 'typing' on a transformed version of it during output.
    for index,value in enumerate(input):
        if value not in keyboard_array:
            raise ValueError("Invalid character found in input string at position %d." % index)

def _find_indices_of_char(search_string: str, char: str) -> np.ndarray:
    # Admittedly this looks a little gross at first glance, but it's hard to argue with results! This index search is crazy fast. Kudos, NumPy.
    str_buffer = np.frombuffer(search_string.encode(), dtype=np.uint8)
    return np.nonzero(str_buffer == ord(char))[0]