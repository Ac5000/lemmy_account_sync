"""Main program to run. Syncs your accounts."""
import configparser
import os
import sys
from pathlib import Path
from time import sleep

from account import Account
from lemmy import Instance
from log_config import configure_logging

# Setup a logger for debugging/outputs.
logger = configure_logging('lemmy_sync')


def get_accounts(config_file: Path) -> list[Account]:
    """Get the accounts from the provided configuration file.

    Args:
        config_file (Path): Path to your config file

    Returns:
        list[Account]: List of Account objects
    """
    config = configparser.ConfigParser()

    logger.info('Reading the config file.')
    read = config.read(config_file)

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


def main():
    """Main code to do the account syncing."""

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
    accounts = get_accounts(cfg_path)

    # Make an Instance object for each account and add to a single list.
    logger.info('Making a list of Lemmy instances.')
    instances: list[Instance] = list()
    for account in accounts:
        instance = Instance(account=account)
        instances.append(instance)

    # Login and get site response for each instance.
    logger.info('Logging into each instance and getting site responses.')
    for instance in instances:
        instance.login()
        # Poor man's rate limiting...
        sleep(0.25)
        instance.get_site_response()

    # Make a combined set of subscribed communities.
    logger.info('Making a combined set of subscriptions.')
    combined_subscriptions: set[str] = set()
    for instance in instances:
        for community in instance.myuserinfo.follows:
            combined_subscriptions.add(community.community.actor_id)

    # Subscribe to each community on each instance.
    for instance in instances:
        for subscription in combined_subscriptions:
            instance.subscribe_to_community(subscription)

    # TODO - Get a site response again, compare against combined and try
    # to subscribe again.


if __name__ == "__main__":
    # Run the code.
    main()
