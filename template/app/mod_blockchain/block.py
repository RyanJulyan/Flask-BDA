
from dataclasses import dataclass
from dataclasses import asdict
from datetime import datetime
import json
import hashlib
import uuid

from app.mod_blockchain.transaction import Transaction


@dataclass
class Block:
    transactions: list[Transaction]
    difficulty: int = 2
    previous_hash: str = str(uuid.uuid4())
    timestamp: datetime = datetime.now()
    nonce: int = 0
    hash_func: str = "sha512"
    _hash: str = ''
    _encoding: str = 'utf-8'

    @property
    def hash(self):
        return self._hash

    @hash.getter
    def hash(self):
        self._hash = self.calculate_hash()
        return self._hash

    def calculate_hash(self):
        """calculate an Encrypted Hash of the transactions

        Returns:
            hexdigest: Encrypted Hash of:
                he previous_hash
                + string of timestamp
                + string of transactions
                + string of nonce
        """
        transaction = (
                    str(self.previous_hash)
                    + self.timestamp.strftime("%Y/%m/%d %H:%M:%S")
                    + json.dumps([asdict(transaction) for transaction in self.transactions])
                    + str(self.nonce)
                )
        h = hashlib.new(self.hash_func)
        h.update(transaction.encode(self._encoding))
        encrypted_transaction = h.hexdigest()

        return encrypted_transaction

    def mine_block(self):
        """This will continue to hash the block until the beginning
            of the hash string matches the `difficulty` * "0"
            e.g. if the `difficulty` is 3 then there should be 3 0's
                at the beginning of the hash:
                000a92e9fb40f0d507ccffa87773260e9d42ef7d48fe1e96...

        Returns:
            hexdigest: Encrypted Hash of:
                he previous_hash
                + string of timestamp
                + string of transactions
                + string of nonce
        """
        while (self._hash[0:self.difficulty] != ("0"*self.difficulty)):
            self.nonce = self.nonce + 1
            self.hash

        return self._hash
