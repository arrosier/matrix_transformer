import numpy as np


def horizontal_flip(matrix: np.ndarray) -> np.ndarray:
    """Reverse the order of elements along axis 0 (left/right)."""

    return np.fliplr(matrix)

def vertical_flip(matrix: np.ndarray) -> np.ndarray:
    """Reverse the order of elements along axis 1 (up/down)."""

    return np.flipud(matrix)

def shift(matrix: np.ndarray, cipher: str, start_index: int, last_index: int) -> np.ndarray:
    """Move all columns left or right by a specified amount."""
    
    shift_amount = _get_shift_amount(cipher, start_index, last_index)
    return np.roll(matrix, shift=shift_amount, axis=1)

def _get_shift_amount(cipher: str, start: int, last_index: int) -> int:
    if start == last_index:
        return int(cipher[start:])
    else:
        end = start + 1
        while True:
            if cipher[end].isdigit():
                if end == last_index:
                    end += 1
                    break
                else:
                    end += 1
            else:
                break
        return int(cipher[start:end])