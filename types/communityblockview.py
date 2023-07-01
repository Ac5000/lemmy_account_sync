"""CommunityBlockView Class"""
from dataclasses import dataclass, field

from .community import Community
from .person import Person


@dataclass
class CommunityBlockView:
    """CommunityBlockView dataclass."""
    person : Person = field(default_factory=Person)
    community : Community = field(default_factory=Community)
