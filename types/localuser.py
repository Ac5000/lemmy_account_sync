"""LocalUser Class"""
from dataclasses import dataclass

from listingtype import ListingType
from sorttype import SortType


@dataclass
class LocalUser:
    """LocalUser dataclass."""
    id: int
    person_id: int
    email: str
    show_nsfw: bool
    theme: str
    default_sort_type: SortType
    default_listing_type: ListingType
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
    totp_2fa_url: str
