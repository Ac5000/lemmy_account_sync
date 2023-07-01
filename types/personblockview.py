"""PersonBlockView Class"""
from dataclasses import dataclass, field

from .person import Person


@dataclass
class PersonBlockView:
    """PersonBlockView dataclass."""
    person: Person = field(default_factory=Person)
    target: Person = field(default_factory=Person)