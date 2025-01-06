"""Similar to the main sync function. But forces all accounts to match
'Main Account'.
"""
import sys
from time import sleep

from account import get_accounts
from instance import Instance
from log_config import configure_logging

# Setup a logger for debugging/outputs.
logger = configure_logging('sync_to_main')


def get_subscriptions(instance: Instance) -> set[str]:
    # Get the set of communities from instance to sync to other accounts.
    logger.info(
        f'Getting set of subscriptions from {instance.account.account}')
    subscriptions: set[str] = set()
    for community in instance.myuserinfo.follows:
        subscriptions.add(community.community.actor_id)
    return subscriptions


def get_blocked_communities(instance: Instance) -> set[str]:
    # Get a set of blocked communities from the instance.
    logger.info(f'Getting blocked communities from {instance.account.account}')
    blocked_communities: set[str] = set()
    for community in instance.myuserinfo.community_blocks:
        blocked_communities.add(community.community.actor_id)
    return blocked_communities


def sync_to_main(sync_user_settings_to_main: bool = True,
                 sync_communities_to_main: bool = False,
                 sync_blocked_communities_to_main: bool = False,
                 sync_blocked_users_to_main: bool = False):
    """Syncs all accounts to the 'Main Account' from the config file."""
    # Get the accounts from the config file.
    accounts = get_accounts()

    # Make an Instance object for each account and add to a single list.
    logger.info('Making a list of Lemmy instances.')
    instances: list[Instance] = list()
    for account in accounts:
        instance = Instance(account=account)
        instance.login()
        # Poor man's rate limiting...
        sleep(0.25)
        instance.get_site_response()

        # Exit early if we can't get the info from main account.
        if (instance.account.account == 'Main Account' and
                (not instance._auth_token or not instance.site_response)):
            logger.error('Failed to login to your "Main Account". Either'
                         ' the instance having issues, or your config file is'
                         ' incorrect. Exiting')
            sys.exit(1)

        # Store off the main account instance for reference.
        if (instance.account.account == 'Main Account' and
                instance._auth_token and instance.site_response):
            main_instance = instance

        # Check for login and response. Otherwise we can't do anything with
        # this instance. Append if good.
        if instance._auth_token and instance.site_response:
            instances.append(instance)

    logger.info('Was able to log in and get responses for'
                f' {len(instances)}/{len(accounts)} accounts.')

    # ---------------------------------------------------------
    # Sync user settings across instances.
    # ---------------------------------------------------------
    # Find the "Main Account" to copy user settings from.
    if sync_user_settings_to_main:
        settings_to_copy = main_instance.get_user_settings()

    # Save main account's user settings to each instance if requested.
    if sync_user_settings_to_main and settings_to_copy:
        logger.info(
            'Syncing user settings from "Main Account" to all instances')
        for instance in instances:
            instance.save_user_settings(settings_to_copy)

    # ---------------------------------------------------------
    # Sync subscribed/followed communities.
    # ---------------------------------------------------------
    if sync_communities_to_main:
        # Sync communities to main.
        communities_to_subscribe = get_subscriptions(main_instance)
    else:
        # Sync communities to combined pool of subscriptions across instances.
        logger.info('Making a combined set of subscriptions.')
        communities_to_subscribe: set[str] = set()
        for instance in instances:
            for community in instance.myuserinfo.follows:
                communities_to_subscribe.add(community.community.actor_id)

    # Subscribe to each community on each instance.
    for instance in instances:
        for subscription in communities_to_subscribe:
            instance.subscribe_to_community(subscription)

    # ---------------------------------------------------------
    # Sync blocked communities across instances.
    # ---------------------------------------------------------
    if sync_blocked_communities_to_main:
        # Sync blocked communities to main.
        communities_to_block = get_blocked_communities(main_instance)

        for instance in instances:
            for community in instance.myuserinfo.community_blocks:
                # Check if we need already blocked this community.
                if community in communities_to_block:
                    continue
                # Check if we need to unblock the community.
                if community not in communities_to_block:
                    # unblock

                    pass

    if not sync_blocked_communities_to_main:
        # Make a combined set of blocked communities.
        logger.info('Making a combined set of blocked communities.')
        communities_to_block: set[str] = set()
        for instance in instances:
            for community in instance.myuserinfo.community_blocks:
                communities_to_block.add(community.community.actor_id)

    if not sync_blocked_communities_to_main:
        # Block each community on each instance.
        for instance in instances:
            for community_url in communities_to_block:
                instance.block_community(community_url)

    # ---------------------------------------------------------
    # Sync blocked users across instances.
    # ---------------------------------------------------------
    # Make a combined set of blocked users.
    logger.info('Making a combined set of blocked users.')
    combined_blocked_users: set[str] = set()
    for instance in instances:
        for user in instance.myuserinfo.person_blocks:
            combined_blocked_users.add(user.target.actor_id)

    # Block each user on each instance.
    for instance in instances:
        for user_url in combined_blocked_users:
            instance.block_person(user_url)

    logger.info('PROGRAM COMPLETE. ACCOUNTS SYNCED TO MAIN ACCOUNT.')


if __name__ == "__main__":
    # Run the code.
    sync_to_main()
