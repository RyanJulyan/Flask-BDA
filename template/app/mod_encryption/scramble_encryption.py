import string


class ScrambleEncryption():
    """ScrambleEncryption is a two way Encryption method that implements the
     a caesar which will 'shift'. .
     A `salt` is added to the message to allow for extra abstraction/prefixing
     of encoded messages.


    :param salt: the salt for the derivation.
    :param salt_multiplier: multiply the salt for extra security.
    :param message_encoding: allows for different text encodings to be used.
                             Defsults to utf-8.
    """

    def __init__(
        self,
        salt: str = "XX",
        salt_multiplier: int = 1,
        shift: int = 7,
    ) -> None:
        super().__init__()
        self.salt = salt * salt_multiplier
        self.shift = shift

    def encrypt(self, message: str) -> str:
        """Change provided message into a secret code (system of letters, numbers, and/or symbols) that people
           cannot understand

        Args:
            message (_type_): a string that we wish to encode/encrypt so that people cannot understand it

        Returns:
            str: An encoded secret code (system of letters, numbers, and/or symbols) that people cannot understand
        """

        encrypted_message = self.caesar(f"{self.salt}|{message}", self.shift)

        return encrypted_message

    def decrypt(self, encoded_message: str) -> str:
        """make (a coded or unclear message) intelligible.

        Args:
            message (str): an encoded string that we wish to decode/decrypt so that people can understand it

        Returns:
            str: An decoded message code (string) that people can understand again
        """
        
        decoded_data = self.caesar(encoded_message, -self.shift)
        decoded_data_without_salt = decoded_data.replace(f"{self.salt}|", "")

        return decoded_data_without_salt

    def caesar(self, plaintext: str, shift: int):

        numbers = string.digits
        shifted_numbers = numbers[shift:] + numbers[:shift]
        table = str.maketrans(numbers, shifted_numbers)
        plaintext = plaintext.translate(table)

        punctuation = string.punctuation
        shifted_punctuation = punctuation[shift:] + punctuation[:shift]
        table = str.maketrans(punctuation, shifted_punctuation)
        plaintext = plaintext.translate(table)

        alphabet = string.ascii_uppercase
        shifted_alphabet = alphabet[shift:] + alphabet[:shift]
        table = str.maketrans(alphabet, shifted_alphabet)
        plaintext = plaintext.translate(table)

        alphabet = string.ascii_lowercase
        shifted_alphabet = alphabet[shift:] + alphabet[:shift]
        table = str.maketrans(alphabet, shifted_alphabet)

        return plaintext.translate(table)
