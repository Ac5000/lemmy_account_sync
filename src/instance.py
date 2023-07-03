"""Instance class for use in lemmy_sync.py"""
import json
import sys
from time import sleep
from types import SimpleNamespace
from urllib.parse import urlparse

import requests

from account import Account
from lem_types import MyUserInfo, SaveUserSettings
from log_config import configure_logging


class Instance:
    """Class that pertains to one Lemmy instance."""
    _api_version = "v3"
    _api_base_url = f"api/{_api_version}"

    def __init__(self, account: Account) -> None:
        # Establish a logger based on the account.
        self.logger = configure_logging(account.account)

        self._auth_token = None
        self.site_response = None
        self.account = account

        # Parse the URL for the site
        parsed_url = urlparse(account.site)
        url_path = parsed_url.netloc if parsed_url.netloc else parsed_url.path
        self._site_url = urlparse(url_path)._replace(scheme='https',
                                                     netloc=url_path,
                                                     path='').geturl()
        self.api_url = f'{self._site_url}/{self._api_base_url}'

    def login(self) -> None:
        """Authenticate to Lemmy instance. Generates self._auth_token"""
        payload = {'username_or_email': self.account.user,
                   'password': self.account.password}

        self.logger.debug(f'Attempting to login to {self._site_url}')

        try:
            req = requests.request(
                method='POST',
                url=f"{self.api_url}/user/login",
                json=payload)
            req.raise_for_status()

            self._auth_token = req.json()['jwt']
            self.logger.debug('Login succeeded.')

        except Exception as exception:
            self.logger.error(f'Login failed for {self.account.user} on'
                              f' {self._site_url}')
            self.logger.error(f'Details: {exception}')
            sys.exit(1)

    def get_site_response(self) -> None:
        """Gets the SiteResponse. Will contain MyUserInfo."""
        self.logger.info('Attempting to get site response.')
        payload = {'auth': self._auth_token}

        try:
            req = requests.request(
                method='GET',
                url=f"{self.api_url}/site",
                params=payload)
            req.raise_for_status()

        except Exception as error:
            self.logger.error('Error getting site response.')
            self.logger.error(f'{error = }')
            return

        self.logger.info('Site response received. Parsing into object.')
        self.site_response = json.loads(
            req.text,
            object_hook=lambda d: SimpleNamespace(**d))

        self.myuserinfo = MyUserInfo(
            self.site_response.my_user.local_user_view,
            self.site_response.my_user.discussion_languages,
            self.site_response.my_user.follows,
            self.site_response.my_user.moderates,
            self.site_response.my_user.community_blocks,
            self.site_response.my_user.person_blocks)

        self.get_user_settings()

    def subscribe_to_community(self, community_url: str) -> bool:
        """Attempts to subscribe to a community from this instance.

        Args:
            community_url (str): URL for the community to subscribe to

        Returns:
            (bool): True for success, False for failed to subscribe
        """
        self.logger.debug(f'Subscribing to "{community_url}" from'
                          f' "{self._site_url}"')

        # Check it's not already subscribed to first.
        for subscribed_community in self.myuserinfo.follows:
            if community_url in subscribed_community.community.actor_id:
                self.logger.debug(f'"{community_url}" already subscribed to.')
                return True

        # Have to figure out/convert the URL into the ID to subscribe.
        community_id = self.resolve_community_id(community_url=community_url)

        if not community_id:
            self.logger.error('Unable to resolve Community ID.'
                              ' Unable to subscribe at this time.')
            return False

        # Rest of this is sending the request to subscribe.
        payload = {'community_id': community_id,
                   'follow': True,
                   'auth': self._auth_token}

        self.logger.debug('Sending the subscribe request.')
        # Poor man's rate limiting...
        sleep(0.25)
        try:
            req = requests.request(
                method='POST',
                url=f"{self.api_url}/community/follow",
                json=payload)
            req.raise_for_status()

        except Exception as error:
            self.logger.error(f'Error subscribing to {community_url}.')
            self.logger.error(f'{error = }')

        # Poor man's rate limiting...
        sleep(0.25)

        if req.status_code == 200:
            self.logger.info(f'Successfully subscribed to {community_url}')
            return True
        else:
            self.logger.warning(f'Failed to subscribe to {community_url}')
            return False

    def resolve_community_id(self, community_url: str) -> int | None:
        """Attempts to resolve the community ID.

        Apparently community IDs are different for each instance?

        Args:
            community_url (str): URL for the community to subscribe to

        Returns:
            (int | None): Community ID if it resolved, otherwise None
        """
        self.logger.debug(f'Resolving {community_url} from {self._site_url}')
        payload = {'q': community_url,
                   'auth': self._auth_token}

        try:
            req = requests.request(
                method='GET',
                url=f"{self.api_url}/resolve_object",
                params=payload)
            req.raise_for_status()

        except Exception as error:
            self.logger.error('Error resolving community ID.')
            self.logger.error(f'{error = }')
            return None

        return req.json()['community']['community']['id']

    def block_community(self, community_url: str) -> bool:
        """Block a community for this instance

        Args:
            community_url (str): Community URL to block

        Returns:
            bool: True if successfully blocked, False if not
        """
        self.logger.debug(f'Blocking {community_url} from {self._site_url}')

        # Check it's not already blocked first.
        for blocked_community in self.myuserinfo.community_blocks:
            if community_url in blocked_community.community.actor_id:
                self.logger.debug(f'"{community_url}" already blocked from'
                                  f' {self._site_url}')
                return True

        # Have to figure out/convert the URL into the ID to block.
        community_id = self.resolve_community_id(community_url=community_url)

        if not community_id:
            self.logger.error('Unable to resolve Community ID.'
                              ' Unable to block at this time.')
            return False

        # Rest of this is sending the request to block.
        payload = {'community_id': community_id,
                   'block': True,
                   'auth': self._auth_token}

        self.logger.debug('Sending the block request.')
        # Poor man's rate limiting...
        sleep(0.25)
        try:
            req = requests.request(
                method='POST',
                url=f"{self.api_url}/community/block",
                json=payload)
            req.raise_for_status()

        except Exception as error:
            self.logger.error(f'Error blocking {community_url}.')
            self.logger.error(f'{error = }')

        # Poor man's rate limiting...
        sleep(0.25)

        if req.status_code == 200:
            self.logger.info(f'Successfully blocked {community_url}')
            return True
        else:
            self.logger.warning(f'Failed to block {community_url}')
            return False

    def resolve_person_id(self, person_url: str) -> int | None:
        """Attempts to resolve the person ID.

        Apparently person IDs are different for each instance?

        Args:
            person_url (str): URL for the person

        Returns:
            (int | None): Person ID if it resolved, otherwise None
        """
        self.logger.debug(f'Resolving {person_url} from {self._site_url}')
        payload = {'q': person_url,
                   'auth': self._auth_token}

        try:
            req = requests.request(
                method='GET',
                url=f"{self.api_url}/resolve_object",
                params=payload)
            req.raise_for_status()

        except Exception as error:
            self.logger.error('Error resolving person ID.')
            self.logger.error(f'{error = }')
            return None

        return req.json()['person']['person']['id']

    def block_person(self, person_url: str) -> bool:
        """Block a person for this instance

        Args:
            person_url (str): Person URL to block

        Returns:
            bool: True if successfully blocked, False if not
        """
        self.logger.debug(f'Blocking {person_url} from {self._site_url}')

        # Check they not already blocked first.
        for blocked_person in self.myuserinfo.person_blocks:
            if person_url in blocked_person.target.actor_id:
                self.logger.debug(f'"{person_url}" already blocked from'
                                  f' {self._site_url}')
                return True

        # Have to figure out/convert the URL into the ID to block.
        person_id = self.resolve_person_id(person_url=person_url)

        if not person_id:
            self.logger.error('Unable to resolve Person ID.'
                              ' Unable to block at this time.')
            return False

        # Rest of this is sending the request to block.
        payload = {'person_id': person_id,
                   'block': True,
                   'auth': self._auth_token}

        self.logger.debug('Sending the block request.')
        # Poor man's rate limiting...
        sleep(0.25)
        try:
            req = requests.request(
                method='POST',
                url=f"{self.api_url}/user/block",
                json=payload)
            req.raise_for_status()

        except Exception as error:
            self.logger.error(f'Error blocking {person_url}.')
            self.logger.error(f'{error = }')

        # Poor man's rate limiting...
        sleep(0.25)

        if req.status_code == 200:
            self.logger.info(f'Successfully blocked {person_url}')
            return True
        else:
            self.logger.warning(f'Failed to block {person_url}')
            return False

    def get_user_settings(self) -> SaveUserSettings:
        """Gets your user settings from the instance."""
        self.logger.info(f'Getting user settings from {self._site_url}')
        if not self._auth_token:
            self.logger.error('No authentication to get settings.')
            return
        self.user_settings = SaveUserSettings(auth=self._auth_token)
        self.user_settings.set_settings(self.myuserinfo.local_user_view.person,
                                        self.myuserinfo.local_user_view.local_user)
        self.logger.info(f'User settings established for {self._site_url}')
        return self.user_settings

    def save_user_settings(self, settings_to_save: SaveUserSettings) -> bool:
        if settings_to_save == self.user_settings:
            self.logger.info(
                f'{self._site_url} user settings already match. Moving on.')
            return True

        self.logger.info(f'Saving user settings to {self._site_url}')
        self.user_settings = settings_to_save
        # Rewriting auth for the settings since it was overwritten in
        # last step.
        self.user_settings.auth = self._auth_token

        try:
            req = requests.request(
                method='PUT',
                url=f"{self.api_url}/user/save_user_settings",
                json=self.user_settings.paylod())
            req.raise_for_status()

        except Exception as error:
            self.logger.error(
                f'Error saving user settings on {self._site_url}.')
            self.logger.error(f'{error = }')

        if req.status_code == 200:
            self.logger.info(
                f'Successfully saved user settings to {self._site_url}')
            return True
        else:
            self.logger.warning(
                f'Failed to save user settings to {self._site_url}')
            return False
