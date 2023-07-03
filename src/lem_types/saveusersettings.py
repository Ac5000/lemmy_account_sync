"""SaveUserSettings Class"""
from dataclasses import dataclass, field

from .listingtype import ListingType
from .localuser import LocalUser
from .person import Person
from .sorttype import SortType


@dataclass
class SaveUserSettings:
    """SaveUserSettings dataclass."""
    auth: str = field(compare=False)
    show_nsfw: bool | None = None
    show_scores: bool | None = None
    theme: str | None = None
    interface_language: str | None = None
    avatar: str | None = field(default=None, compare=False)
    banner: str | None = field(default=None, compare=False)
    display_name: str | None = None
    email: str | None = None
    bio: str | None = None
    matrix_user_id: str | None = None
    show_avatars: bool | None = None
    send_notifications_to_email: bool | None = None
    bot_account: bool | None = None
    show_bot_accounts: bool | None = None
    show_read_posts: bool | None = None
    show_new_post_notifs: bool | None = None
    generate_totp_2fa: bool | None = None
    default_listing_type: ListingType | None = None
    default_sort_type: SortType | None = None
    discussion_languages: list[int] | None = None

    def set_settings(self, person: Person, localuser: LocalUser) -> None:
        """Sets the attribute values based on incoming variables.

        Args:
            person (Person): MyUserInfo Person response from instance
            localuser (LocalUser): MyUserInfo LocalUser response from instance
        """
        # Set all the SaveUserSettings attributes that we find.
        for item in vars(self).items():
            # Get values from Person
            if item[0] in vars(person).keys():
                setattr(self, item[0], getattr(person, item[0]))
            # Get values from LocalUser
            if item[0] in vars(localuser).keys():
                setattr(self, item[0], getattr(localuser, item[0]))

    def paylod(self) -> dict:
        """Generates a payload to send to update your user settings.

        Returns:
            dict: Payload to send for updating user settings.
        """
        payload = dict()
        # Don't think you can save/point to another image? Might try later.
        attributes_to_ignore: list[str] = ['avatar', 'banner']
        for item in vars(self).items():
            if item[1] is not None and item[0] not in attributes_to_ignore:
                payload.update([item])
        return payload
