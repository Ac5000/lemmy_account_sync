"""MyUserInfo Class"""
from dataclasses import dataclass, field

from .communityblockview import CommunityBlockView
from .communityfollowerview import CommunityFollowerView
from .communitymoderatorview import CommunityModeratorView
from .localuserview import LocalUserView
from .personblockview import PersonBlockView


@dataclass
class MyUserInfo:
    """MyUserInfo dataclass."""
    local_user_view: LocalUserView
    follows: list[CommunityFollowerView] = field(
        default_factory=list[CommunityFollowerView])
    moderates:list[CommunityModeratorView] = field(
        default_factory=list[CommunityModeratorView])
    community_blocks: list[CommunityBlockView] = field(
        default_factory=list[CommunityBlockView])
    person_blocks: list[PersonBlockView] = field(
        default_factory=list[PersonBlockView])
    discussion_languages: int