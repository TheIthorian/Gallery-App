import unittest

from encryption import encrypt

class TestEncryption(unittest.TestCase):

    def test_encrypt():
        # Given
        filename = 'filename.txt'
        file_data = 'file_data'
        key = b'key'
        
        # When
        result = encrypt(filename, file_data, key)

        # Then
        assert result == '123'

