"""Account class."""
from dataclasses import dataclass


@dataclass
class Account:
    account: str
    site: str
    user: str
    password: str
