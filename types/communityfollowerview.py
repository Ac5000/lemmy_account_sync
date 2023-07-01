"""CommunityFollowerView Class"""
from dataclasses import dataclass, field

from.community import Community
from .person import Person


@dataclass
class CommunityFollowerView:
    """CommunityFollowerView dataclass."""
    community: Community = field(default_factory=Community)
    follower: Person = field(default_factory=Person)