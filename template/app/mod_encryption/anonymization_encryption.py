import binascii
import hashlib


class AnonymizationEncryption():
    """AnonymizationEncryption is a one way Encryption method that implements the
     standard hashlib.pbkdf2_hmac method with the given `salt`.
     It iterates `iterations` times and produces an anonymized string.
     By default, SHA-512 is used as hash function;
     A different hashlib `hashfunc` can be provided.


    :param salt: the salt for the derivation.
    :param salt_multiplier: multiply the salt for extra security.
    :param message_encoding: allows for different text encodings to be used.
                             Defsults to utf-8.
    :param app_iters: the number of iterations.
                      for more details: https://security.stackexchange.com/questions/3959/recommended-of-iterations-when-using-pbkdf2-sha256/
                      Defaults to 1_750_000
    :param hashfunc: the hash function to use.  This must be the
                     string name of a known hash function from hashlib
                     Defaults to sha512.
    """

    def __init__(
        self,
        salt: str,
        salt_multiplier: int = 5,
        app_iters: int = 1_750_000,
        hashfunc: str = "sha512",
        message_encoding: str = "utf-8",
    ) -> None:
        super().__init__()
        self.salt = (salt * salt_multiplier).encode(
            message_encoding
        )  # 'salt_multiplier' Not saved for Attr Security but can be figured out
        self.app_iters = app_iters
        self.hashfunc = hashfunc
        self.message_encoding = message_encoding

    def encrypt(self, message: str) -> str:
        """Change provided message into a secret code (system of letters, numbers, and/or symbols) that people
           cannot understand

        Args:
            message (_type_): a string that we wish to encode/encrypt so that people cannot understand it

        Returns:
            str: An encoded secret code (system of letters, numbers, and/or symbols) that people cannot understand
        """

        encrypted_message = (
            binascii.b2a_base64(
                hashlib.pbkdf2_hmac(
                    self.hashfunc,
                    message.encode(self.message_encoding),
                    self.salt,
                    self.app_iters,
                )
            )
            .strip()
            .decode(self.message_encoding)
        )

        return encrypted_message

    def decrypt(self, encoded_message: str) -> str:
        """make (a coded or unclear message) intelligible.

        Args:
            message (str): an encoded string that we wish to decode/decrypt so that people can understand it

        Returns:
            Exception: AnonymizationEncryption is a one way Encryption method
        """

        raise Exception(
            "Sorry, AnonymizationEncryption is a one way Encryption method and you\
                 cannot decrypt a message using this class"
        )
