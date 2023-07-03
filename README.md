# **WARNING!!! THIS IS A WORK IN PROGRESS.**  

Feel free to use what I have. I am still working on it though.  

I am open to suggestions. Also open to feedback since I am always learning how to code.

## Sync Your Subscribed Lemmy Communities Between Multiple Accounts

This program will look at multiple accounts and try to sync them up.  

Will let you treat different Lemmy instances like it's all one shared account in case your favorite instance is down, or to more easily move when needed.

## Things That Should Get Synced

1. Subscribed Communities
2. Blocked Communities
3. Blocked Users
4. Account Settings

## Configuration

The program is controlled by a configuration file. See "exampleconfig.ini" for an example of the format.

Copy the "exampleconfig.ini" file, paste it in the "src" folder, and rename to "myconfig.ini" and fill in your accounts like the example shows.

You can have as many accounts as you wish. Labels for accounts can be anything except "Default".

Whatever account has the name "Main Account" will be the source for syncing your user settings since I don't know how to tell which account has the most recent updates.

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
Run "lemmy_sync.py" after creating and updating the configuration file.

You will need the "Requests" package at minimum to run.

pip install -r requirements.txt just to run the application.

pip install -r dev_requirements.txt if you want to follow same formatting/structure to contribute.
```

## Thank You

Special thanks to <https://github.com/wescode/lemmy_migrate> for giving me the inspiration and base code to build from.

Thanks to <https://github.com/LemmyNet/lemmy-js-client> for having the types and URLs laid out well enough that I could reverse engineer it.

## Other Notes

Unit tests aren't working/non-existant at the moment. So basically ignore the "tests" directory...

Feel free to contribute or make requests. This is a side project that I mostly did for myself, but I would love to help more people if I can. I won't guarantee I will get the time to fix anything though...
