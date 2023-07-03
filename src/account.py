"""Account class."""
from dataclasses import dataclass


@dataclass
class Account:
    """Account dataclass.
    """
    account: str
    site: str
    user: str
    password: str
