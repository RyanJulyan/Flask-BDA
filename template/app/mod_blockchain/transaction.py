from dataclasses import dataclass


@dataclass
class Transaction:
    from_address: str
    to_address: str
    data: dict[str: dict]
    amount: float = 0
