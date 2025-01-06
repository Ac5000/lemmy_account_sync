"""Unit tests for lemmy.py"""
import os
import unittest
from pathlib import Path

from src.lemmy_sync import get_accounts


class TestLemmySync(unittest.TestCase):
    """Main test case."""

    def test_get_accounts(self):
        """Test get_accounts function."""
        expected_results = {'Main Account':
                            {'site': 'https://sh.itjust.works',
                             'user': 'Imauser',
                             'password': 'apasswod'},
                            'Account 2':
                            {'site': 'https://lemmy.ml',
                             'user': 'cooluser',
                             'password': 'badpassword'}}

        test_config = Path(os.path.dirname(__file__),
                           'test_files',
                           'testconfig.ini')
        accounts = get_accounts(test_config)

        self.assertEqual(accounts, expected_results)
