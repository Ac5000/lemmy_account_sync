"""Account class."""
from dataclasses import dataclass, field


@dataclass
class Account:
    """Account dataclass.
    """
    account: str
    site: str
    user: str
    password: str = field(repr=False)
