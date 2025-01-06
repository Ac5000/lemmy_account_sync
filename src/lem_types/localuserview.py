"""LocalUserView Class"""
from dataclasses import dataclass, field

from .localuser import LocalUser
from .person import Person
from .personaggregates import PersonAggregates


@dataclass
class LocalUserView:
    """LocalUserView dataclass."""
    local_user: LocalUser = field(default_factory=LocalUser)
    person: Person = field(default_factory=Person)
    counts: PersonAggregates = field(default_factory=PersonAggregates)