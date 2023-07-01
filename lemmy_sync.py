"""Main program to run. Syncs your accounts."""
import configparser
import sys
from pathlib import Path

from lemmy import Lemmy
from log_config import configure_logging

# Setup a logger for debugging/outputs.
logger = configure_logging('lemmy_sync')


def get_accounts(config_file: Path):
    """Get the accounts from the provided configuration file.

    Args:
        config_file (Path): Path to your config file

    Returns:
        dict[str, dict[str, str]]: Dictionary of accounts and logins
    """
    config = configparser.ConfigParser()

    logger.info('Reading the config file.')
    read = config.read(config_file)

    if not read:
        logger.error('Could not read the config file. Check the formatting'
                     ' matches the "exampleconfig.ini".')
        logger.info('Program exiting.')
        sys.exit(1)

    accounts = {i: dict(config.items(i)) for i in config.sections()}

    logger.info('Found the following accounts:')
    for acc in accounts:
        logger.info(
            f'"{acc}" {accounts[acc]["user"]} at {accounts[acc]["site"]}')
    return accounts


def get_account_communities(site: str, user: str, password: str):
    """Gets the list of subscribed communities for a site/account.

    Args:
        site (str): Lemmy site/address/url
        user (str): Account username
        password (str): Account password
    """
    lemming = Lemmy(site)
    lemming.login(user=user, password=password)
    communties = lemming.get_communities()
    logger.info(f'{len(communties)} communities subscribed to on {site}.')
    return communties


def main():
    """Main code to do the account syncing."""

    # Establish a base Path to your config file.
    cfg_path = Path('myconfig.ini')

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

    # TEST
    # communties = get_account_communities(accounts['Main Account']['site'],
    #                                      accounts['Main Account']['user'],
    #                                      accounts['Main Account']['password'])

    # Get combined list of subscribed communities between all accounts.
    combined_subscribed_communities = dict()
    for acc in accounts:
        instance_communities = get_account_communities(accounts[acc]['site'],
                                                       accounts[acc]['user'],
                                                       accounts[acc]['password'])
        combined_subscribed_communities |= instance_communities

    print('test')
    # source site
    logger.info(
        f"Getting Account Info - {accounts['Main Account']['site']} ]")
    lemming = Lemmy(accounts['Main Account']['site'])
    lemming.login(accounts['Main Account']['user'],
                  accounts['Main Account']['password'])
    communties = lemming.get_communities()
    print(f" {len(communties)} subscribed communities found")
    accounts.pop('Main Account', None)

    # sync main account communities to each account
    for acc in accounts:
        print(f"\n[ Syncing {acc} - {accounts[acc]['site']} ]")
        new_lemming = Lemmy(accounts[acc]['site'])
        new_lemming.login(accounts[acc]['user'], accounts[acc]['password'])
        comms = new_lemming.get_communities()
        print(f" {len(comms)} subscribed communities found")
        new_communities = {c: communties[c]
                           for c in communties if c not in comms}

        if new_communities:
            print(f" Subscribing to {len(new_communities)} new communities")
            new_lemming.subscribe(new_communities)


if __name__ == "__main__":
    # Run the code.
    main()
