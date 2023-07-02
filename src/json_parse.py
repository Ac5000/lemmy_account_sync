"""Can I take the initial site view and parse it?"""
import json
import os
from types import SimpleNamespace
from pathlib import Path

from lem_types import MyUserInfo

# Location to a test file.
path_to_file = Path(
    r'C:/Users/burns/OneDrive/Documents/Lemmy_Account_Sync/lemmy_world_siteview.json')

# Read the saved test file
with path_to_file.open(encoding='utf-8') as f_:

    # Load the JSON data into a simplenamespace
    load = json.load(f_, object_hook=lambda d: SimpleNamespace(**d))

myuserinfo = MyUserInfo(load.my_user.local_user_view,
                        load.my_user.discussion_languages,
                        load.my_user.follows,
                        load.my_user.moderates,
                        load.my_user.community_blocks,
                        load.my_user.person_blocks)


# print(load['my_user'])

print(myuserinfo.community_blocks[1].community.id)

for community_to_block in myuserinfo.community_blocks:
    print(f'ID={community_to_block.community.id} and name='
          f' {community_to_block.community.name}')


print('done')
