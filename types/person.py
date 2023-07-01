"""Person Class"""
from dataclasses import dataclass


@dataclass
class Person:
    """Person dataclass."""
    id: int
    name: str
    display_name: str
    avatar: str
    banned: bool
    published: str
    updated: str
    actor_id: str
    bio: str
    local: bool
    banner: str
    deleted: bool
    matrix_user_id: str
    admin: bool
    bot_account: bool
    ban_expires: str
    instance_id: int