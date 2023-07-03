"""LocalUser Class"""
from dataclasses import dataclass, field

from .listingtype import ListingType
from .sorttype import SortType


@dataclass
class LocalUser:
    """LocalUser dataclass."""
    id: int
    person_id: int
    show_nsfw: bool
    theme: str
    interface_language: str
    show_avatars: bool
    send_notifications_to_email: bool
    validator_time: str
    show_scores: bool
    show_bot_accounts: bool
    show_read_posts: bool
    show_new_post_notifs: bool
    email_verified: bool
    accepted_application: bool
    email: str | None = None
    totp_2fa_url: str | None = None
    default_sort_type: SortType = field(default_factory=SortType)
    default_listing_type: ListingType = field(default_factory=ListingType)
