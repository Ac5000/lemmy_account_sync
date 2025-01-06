"""Account class and get_accounts function."""
import configparser
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from log_config import configure_logging

# Setup a logger for debugging/outputs.
logger = configure_logging('account')


@dataclass
class Account:
    """Account dataclass.
    """
    account: str
    site: str
    user: str
    password: str = field(repr=False)


def get_accounts() -> list[Account]:
    """Get the accounts from the configuration file.

    Returns:
        list[Account]: List of Account objects
    """
    # Establish a base Path to the config file.
    cfg_path = Path(os.path.dirname(__file__), 'myconfig.ini')

    # Verify the config file exists. Provide error message and exit
    # if it doesn't.
    if not cfg_path.is_file():
        logger.error(f'File "{cfg_path}" does not exist. Please copy and'
                     ' paste the "exampleconfig.ini" file, rename it to'
                     ' "myconfig.ini" and fill it out with your information.')
        logger.info('Program exiting.')
        sys.exit(1)

    # Get the accounts from the config file.
    config = configparser.ConfigParser(interpolation=None)

    logger.info('Reading the config file.')
    read = config.read(cfg_path)

    if not read:
        logger.error('Could not read the config file. Check the formatting'
                     ' matches the "exampleconfig.ini".')
        logger.info('Program exiting.')
        sys.exit(1)

    accounts: list[Account] = list()

    # Read config into list of account objects.
    for i in config.sections():
        items = dict(config.items(i))
        account = Account(account=i,
                          site=items['site'],
                          user=items['user'],
                          password=items['password'])
        accounts.append(account)

    logger.info('Found the following accounts:')
    for acc in accounts:
        logger.info(acc)
    return accounts
