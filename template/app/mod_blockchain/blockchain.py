from dataclasses import dataclass
import uuid

from app.mod_blockchain.block import Block
from app.mod_blockchain.transaction import Transaction


@dataclass
class BlockChain:
    difficulty = 2
    miningReward = 1
    pending_transactions: list[Block] = None
    chain: list[Block] = None
    __init_previous_hash: str = None

    def __post_init__(self):
        """
        Default class attribute values
        """
        self.__init_previous_hash = str(uuid.uuid4())
        if (
            self.chain is None
            or self.chain == []
        ):
            self.chain = [self.create_root_block()]
        
        if (
            self.pending_transactions is None
            or self.pending_transactions == []
        ):
            self.pending_transactions = []


    def create_root_block(self):
        return Block(
            transactions=[],
            difficulty=self.difficulty,
            previous_hash=self.__init_previous_hash
        )

    def get_latest_block(self):
        return self.chain[len(self.chain) - 1]

    def mine_pending_transactions(self, mining_reward_address: str):
        reward = Transaction(
            None,
            mining_reward_address,
            {"message": "Verifying transactions"},
            self.miningReward
        )
        self.pending_transactions.append(reward)

        block = Block(
            transactions=self.pending_transactions,
            difficulty=self.difficulty,
            previous_hash=self.get_latest_block().hash
        )
        block.mine_block()

        print('Block successfully mined!')
        self.chain.append(block)

        self.pending_transactions = []

    def create_transaction(self, transaction: Transaction):
        self.pending_transactions.append(transaction)

    def get_balance_of_address(self, address: str):
        balance = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction.from_address == address:
                    balance -= transaction.amount

                if transaction.to_address == address:
                    balance += transaction.amount

        return balance

    def is_chain_valid(self):
        for i in range(0, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            
            if i == 0 and current_block.previous_hash == self.__init_previous_hash:
                return True
            elif current_block.previous_hash != previous_block.calculate_hash():
                return False

        return True
