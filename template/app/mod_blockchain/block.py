
from dataclasses import dataclass
from datetime import datetime

import json
import hashlib
import uuid


@dataclass
class Block:
    messages: list[dict[str:dict]]
    timestamp: datetime = datetime.now()
    previousHash: str = str(uuid.uuid4())
    nonce: int = 0
    difficulty: int = 4
    hashfunc: str = "sha512"
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
        
        message = (
                    str(self.previousHash)
                    + self.timestamp.strftime("%Y/%m/%d %H:%M:%S")
                    + json.dumps(self.messages)
                    + str(self.nonce)
                )
        h = hashlib.new(self.hashfunc)
        h.update(message.encode(self._encoding))
        encrypted_message = h.hexdigest()

        return encrypted_message

    def mine_block(self):
        while (self._hash[0:self.difficulty] != ("0"*self.difficulty)):
            self.nonce = self.nonce + 1
            self.hash
        
        return self._hash
