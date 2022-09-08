import base64


class PseudoAnonymizationEncryption():
    """PseudoAnonymizationEncryption is a two way Encryption method that implements the
     standard base64 library. A `salt` is added to the message to allow for extra security
     of encoded messages.


    :param salt: the salt for the derivation.
    :param salt_multiplier: multiply the salt for extra security.
    :param message_encoding: allows for different text encodings to be used.
                             Defsults to utf-8.
    """

    def __init__(
        self,
        salt: str,
        salt_multiplier: int = 5,
        message_encoding: str = "utf-8",
    ) -> None:
        super().__init__()
        self.salt = (salt * salt_multiplier).encode(
            message_encoding
        )  # 'salt_multiplier' Not saved for Attr Security but can be figured out
        self.message_encoding = message_encoding

    def encrypt(self, message: str) -> str:
        """Change provided message into a secret code (system of letters, numbers, and/or symbols) that people
           cannot understand

        Args:
            message (_type_): a string that we wish to encode/encrypt so that people cannot understand it

        Returns:
            str: An encoded secret code (system of letters, numbers, and/or symbols) that people cannot understand
        """

        encrypted_message = base64.b64encode(
            (f"{message}|{self.salt}").encode(self.message_encoding)
        ).decode(self.message_encoding)

        return encrypted_message

    def decrypt(self, encoded_message: str) -> str:
        """make (a coded or unclear message) intelligible.

        Args:
            message (str): an encoded string that we wish to decode/decrypt so that people can understand it

        Returns:
            str: An decoded message code (string) that people can understand again
        """
        decoded_data = base64.b64decode(encoded_message).decode(self.message_encoding)
        decoded_data_without_salt = decoded_data.replace(f"|{self.salt}", "")

        return decoded_data_without_salt
