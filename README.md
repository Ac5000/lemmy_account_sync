# Sync Your Subscribed Lemmy Communities Between Multiple Accounts

This program will look at multiple accounts, figure out a master list of communities between them, and make sure all accounts are subscribed to the same communities.

## Configuration

The program is controlled by a configuration file. See "exampleconfig.ini" for an example of the format.

Copy, paste, and rename to "myconfig.ini" and fill in your accounts.

You can have as many accounts as you wish. Labels for accounts can be anything.

```ini
[Main Account]
Site = https://sh.itjust.works
User = Imauser
Password = apasswod

[Account 2]
Site = https://lemmy.ml
User = cooluser
Password = badpassword
```

## Usage

```text
Run lemmy_sync.py after creating and updating the configuration file.
```
