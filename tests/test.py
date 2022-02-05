import unittest

import numpy as np

from matrix_transformer import transformer, operations, validation


KEYBOARD_ARRAY = np.array([
        ['1','2','3','4','5','6','7','8','9','0'],
        ['Q','W','E','R','T','Y','U','I','O','P'],
        ['A','S','D','F','G','H','J','K','L',';'],
        ['Z','X','C','V','B','N','M',',','.','/']
        ])
TEST_MATRIX = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
TEST_INPUT = "DOG"


class TestValidationMethods(unittest.TestCase):
    def test_validateLegalCharacters_badCharactersPresent_raisesException(self):
        ciphers = ["HVS2HVVHD","S12S-3QN17","hvs3","VS18~H",""]
        for c in ciphers:
            with self.subTest():
                self.assertRaises(ValueError, validation.validate_legal_characters, c)
    
    def test_validateShiftOperator_notFollowedByNumberOrNegative_raisesException(self):
        cipher = "HVSV"
        self.assertRaises(ValueError, validation.validate_shift_operator, cipher)

    def test_validateMiscellaneousCharacters_cipherStartsWithMinus_raisesException(self):
        cipher = "-HS2S-23"
        self.assertRaises(ValueError, validation.validate_miscellaneous_characters, cipher)
    
    def test_validateMiscellaneousCharacters_cipherEndsWithMinus_raisesException(self):
        cipher = "VHS2-"
        self.assertRaises(ValueError, validation.validate_miscellaneous_characters, cipher)
    
    def test_validateMiscellaneousCharacters_minusNotBeforeNumber_raisesException(self):
        ciphers = ["HVS--2","VS-HS-12","HV-2S8"]
        for c in ciphers:
            with self.subTest():
                self.assertRaises(ValueError, validation.validate_miscellaneous_characters, c)
    
    def test_validateInputString_inputContainsCharactersNotOnKeyboard_raisesException(self):
        inputs = ["ANCHL~Q","+SVH",""]
        for i in inputs:
            with self.subTest():
                self.assertRaises(ValueError, validation.validate_input_string, KEYBOARD_ARRAY, i)
    
    def test_findIndicesOfChar_stringContainsChar_returnsCorrectIndices(self):
        test_string = "ABCDEFC"
        search_char = 'C'
        result = validation._find_indices_of_char(test_string, search_char)
        expected_result = np.array([2,6])
        self.assertIn(result, expected_result)

    def test_findIndicesOfChar_stringDoesNotContainChar_returnsEmpty(self):
        test_string = "ABDEF"
        search_char = 'C'
        result = validation._find_indices_of_char(test_string, search_char)
        expected_result = np.array([])
        np.testing.assert_array_equal(result, expected_result)


class TestOperationMethods(unittest.TestCase):
    def test_horizontalFlip_operationPerformed_correctResult(self):
        result = operations.horizontal_flip(TEST_MATRIX)
        expected_result = np.array([[3,2,1],[6,5,4],[9,8,7],[12,11,10]])
        np.testing.assert_array_equal(result, expected_result)
    
    def test_verticalFlip_operationPerformed_correctResult(self):
        result = operations.vertical_flip(TEST_MATRIX)
        expected_result = np.array([[10,11,12],[7,8,9],[4,5,6],[1,2,3]])
        np.testing.assert_array_equal(result,expected_result)

    def test_shift_positiveShift_correctResult(self):
        cipher = "S2"
        index = 1
        last_index = 1
        result = operations.shift(TEST_MATRIX, cipher, index, last_index)
        expected_result = np.array([[2,3,1],[5,6,4],[8,9,7],[11,12,10]])
        np.testing.assert_array_equal(result,expected_result)
    
    def test_shift_negativeShift_correctResult(self):
        cipher = "S-2"
        index = 1
        last_index = 1
        result = operations.shift(TEST_MATRIX, cipher, index, last_index)
        expected_result = np.array([[3,1,2],[6,4,5],[9,7,8],[12,10,11]])
        np.testing.assert_array_equal(result,expected_result)

    def test_getShiftAmount_singleDigitPositiveNumber_returnsCorrectAmount(self):
        cipher = "S3"
        index = 1
        last_index = 1
        result = operations._get_shift_amount(cipher, index, last_index)
        expected_result = 3
        self.assertEqual(result, expected_result)

    def test_getShiftAmount_singleDigitNegativeNumber_returnsCorrectAmount(self):
        cipher = "S-3"
        index = 1
        last_index = 2
        result = operations._get_shift_amount(cipher, index, last_index)
        expected_result = -3
        self.assertEqual(result, expected_result)

    def test_getShiftAmount_multiDigitNumber_returnsCorrectAmount(self):
        cipher = "S123"
        index = 1
        last_index = 3
        result = operations._get_shift_amount(cipher, index, last_index)
        expected_result = 123
        self.assertEqual(result, expected_result)

    def test_getShiftAmount_multiDigitNegativeNumber_returnsCorrectAmount(self):
        cipher = "S-123"
        index = 1
        last_index = 4
        result = operations._get_shift_amount(cipher, index, last_index)
        expected_result = -123
        self.assertEqual(result, expected_result)


class TestTransformerMethods(unittest.TestCase):
    def test_transform_performTransformation_correctResult(self):
        cipher = "HVS1"
        result = transformer._transform(TEST_MATRIX, cipher)
        expected_result = np.array([[10,12,11],[7,9,8],[4,6,5],[1,3,2]])
        np.testing.assert_array_equal(result, expected_result)

    def test_getOutput_retypeAfterTransform_returnsCorrect(self):
        new_matrix = transformer._transform(KEYBOARD_ARRAY, "S1")
        result = transformer._get_output(KEYBOARD_ARRAY, new_matrix, TEST_INPUT)
        expected_result = "SIF"
        self.assertEqual(result, expected_result)

    def test_execute_performExecution_correctResult(self):
        cipher = "HS2"
        input = "DOG"
        expected_result = ";RK"
        result = transformer.execute(KEYBOARD_ARRAY, cipher, input)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()