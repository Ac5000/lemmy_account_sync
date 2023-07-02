# **WARNING!!! THIS IS A WORK IN PROGRESS.**  

Feel free to use what I have. I'm still working on it though.  

I'm open to suggestions. Also open to feedback since I'm always learning how to code.

## Sync Your Subscribed Lemmy Communities Between Multiple Accounts

This program will look at multiple accounts and try to sync them up.  

Will let you treat different Lemmy instances like it's all one shared account in case your favorite instance is down, or to more easily move when needed.

## Things to sync

1. Subscribed communities
2. Blocked communities
3. Blocked users
4. Account settings

## Configuration

The program is controlled by a configuration file. See "exampleconfig.ini" for an example of the format.

Copy, paste, and rename to "myconfig.ini" and fill in your accounts.

You can have as many accounts as you wish. Labels for accounts can be anything except "Default".

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

## Thank you

Special thanks to <https://github.com/wescode/lemmy_migrate> for giving me the inspiration and base code to build from.
