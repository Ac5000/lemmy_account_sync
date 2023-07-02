"""Lemmy class for use in lemmy_migrate.py"""
import sys
from collections import defaultdict
from time import sleep
from urllib.parse import urlparse

import requests

from log_config import configure_logging


class Lemmy:
    """Lemmy class for use in the migration."""
    _api_version = "v3"
    _api_base_url = f"api/{_api_version}"

    def __init__(self, url: str) -> None:
        parsed_url = urlparse(url)
        url_path = parsed_url.netloc if parsed_url.netloc else parsed_url.path
        self._site_url = urlparse(url_path)._replace(scheme='https',
                                                     netloc=url_path,
                                                     path='').geturl()
        self._auth_token = None
        self._user_communities = defaultdict(dict)
        self.logger = configure_logging(url)

    def login(self, user: str, password: str) -> None:
        """Authenticate to Lemmy instance. Generates self._auth_token

        Args:
            user (str): Username to use for login
            password (str): Password to use for login
        """
        payload = {
            'username_or_email': user,
            'password': password
        }

        self.logger.debug(f'Attempting to login to {self._site_url}')

        try:
            resp = self._request_it(
                f"{self._site_url}/{self._api_base_url}/user/login",
                method='POST', json=payload)
            self._auth_token = resp.json()['jwt']
            self.logger.debug('Login succeeded.')
        except Exception as exception:
            self.logger.error(f"Login failed for {user} on {self._site_url}")
            self.logger.error(f"Details: {exception}")
            sys.exit(1)

    def get_communities(self, type_: str = "Subscribed") -> dict:
        """Get list of currently subscribed communites"""
        payload = {
            'type_': type_,
            'auth': self._auth_token,
            'limit': 50,
            'page': 1
        }

        # iterate over each page if needed
        fetched = 50  # max limit
        while fetched == 50:
            try:
                resp = self._request_it(
                    f"{self._site_url}/{self._api_base_url}/community/list",
                    params=payload)
                fetched = len(resp.json()['communities'])
                payload['page'] += 1

                for comm in resp.json()['communities']:
                    id_ = comm['community']['id']
                    url = comm['community']['actor_id']
                    self._user_communities[url]['id'] = id_
            except Exception as err:
                print(f"error: {err}")

        return self._user_communities

    def subscribe(self, communities: dict = None) -> None:
        """Subscribe to a community. It will first attempt to resolve community."""
        if communities:
            self._user_communities = communities
        else:
            self.get_communities()

        payload = {
            'community_id': None,
            'follow': True,
            'auth': self._auth_token
        }

        for url, _cid in self._user_communities.items():
            try:
                # resolve community first
                comm_id = self.resolve_community(url)

                if comm_id:
                    payload['community_id'] = comm_id
                    self._println(2, f"> Subscribing to {url} ({comm_id})")
                    resp = self._request_it(
                        f"{self._site_url}/{self._api_base_url}/community/follow",
                        json=payload, method='POST')

                    if resp.status_code == 200:
                        self._println(
                            3, f"> Succesfully subscribed to {url} ({comm_id})")
            except Exception as exception:
                print(f"   API error: {exception}")

    def resolve_community(self, community: str) -> int | None:
        """resolve a community"""
        payload = {
            'q': community,
            'auth': self._auth_token
        }

        community_id = None
        self._println(1, f"> Resolving {community}")
        try:
            resp = self._request_it(
                f"{self._site_url}/{self._api_base_url}/resolve_object",
                params=payload)
            community_id = resp.json()['community']['community']['id']
        except Exception as exception:
            self._println(2, f"> Failed to resolve community. {exception}")

        return community_id

    def _rate_limit(self):
        sleep(1)

    def _request_it(self,
                    endpoint: str,
                    method: str = 'GET',
                    params: str = None,
                    json: dict = None) -> requests.Response:

        self._rate_limit()
        try:
            req = requests.request(method,
                                   url=endpoint,
                                   params=params,
                                   json=json)
            req.raise_for_status()
            return req
        except requests.exceptions.HTTPError:
            raise
        except requests.exceptions.RequestException:
            raise

    def _println(self, indent, line):
        print(f"{' ' * indent}{line}")
