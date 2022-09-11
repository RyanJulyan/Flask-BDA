from binascii import hexlify
from hashlib import sha256
from os import urandom

from app.mod_encryption.primes import primes


class DiffieHellmanEncryption:
    # Current minimum recommendation is 2048 bit (encoding_bit 14)
    def __init__(self, encoding_bit: int = 14) -> None:
        if encoding_bit not in primes:
            raise ValueError("Unsupported encoding_bit")
        self.prime = primes[encoding_bit]["prime"]
        self.generator = primes[encoding_bit]["generator"]

        self.__private_key = int(hexlify(urandom(32)), base=16)

    def get_private_key(self) -> str:
        return hex(self.__private_key)[2:]

    def generate_public_key(self) -> str:
        public_key = pow(self.generator, self.__private_key, self.prime)
        return hex(public_key)[2:]

    def is_valid_public_key(self, key: int) -> bool:
        # check if the other public key is valid based on NIST SP800-56
        if 2 <= key and key <= self.prime - 2:
            if pow(key, (self.prime - 1) // 2, self.prime) == 1:
                return True
        return False

    def generate_shared_key(self, other_key_str: str) -> str:
        other_key = int(other_key_str, base=16)
        if not self.is_valid_public_key(other_key):
            raise ValueError("Invalid public key")
        shared_key = pow(other_key, self.__private_key, self.prime)
        return sha256(str(shared_key).encode()).hexdigest()
    
    @staticmethod
    def is_valid_public_key_static(
        local_private_key_str: str, remote_public_key_str: str, prime: int
    ) -> bool:
        # check if the other public key is valid based on NIST SP800-56
        if 2 <= remote_public_key_str and remote_public_key_str <= prime - 2:
            if pow(remote_public_key_str, (prime - 1) // 2, prime) == 1:
                return True
        return False

    @staticmethod
    def generate_shared_key_static(
        local_private_key_str: str, remote_public_key_str: str, encoding_bit: int = 14
    ) -> str:
        local_private_key = int(local_private_key_str, base=16)
        remote_public_key = int(remote_public_key_str, base=16)
        prime = primes[encoding_bit]["prime"]
        if not DiffieHellman.is_valid_public_key_static(
            local_private_key, remote_public_key, prime
        ):
            raise ValueError("Invalid public key")
        shared_key = pow(remote_public_key, local_private_key, prime)
        return sha256(str(shared_key).encode()).hexdigest()

    @staticmethod
    def xor_encrypt_decrypt(message: str, key_string: str):
        key = list(key_string)
        output = []
        for i in range(len(message)):
            char_code = ord(message[i]) ^ ord(key[i % len(key)][0])
            output.append(chr(char_code))
        return "".join(output)

    @staticmethod
    def encrypt(message: str, key: str):
        return DiffieHellman.xor_encrypt_decrypt(message, key)

    @staticmethod
    def decrypt(encrypted_message: str, key: str):
        return DiffieHellman.xor_encrypt_decrypt(encrypted_message, key)
