"""CommunityModeratorView Class"""
from dataclasses import dataclass, field

from .community import Community
from .person import Person


@dataclass
class CommunityModeratorView:
    """CommunityModeratorView dataclass."""
    community: Community = field(default_factory=Community)
    moderator: Person = field(default_factory=Person)