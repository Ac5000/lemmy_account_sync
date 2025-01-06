"""Person Class"""
from dataclasses import dataclass


@dataclass
class Person:
    """Person dataclass."""
    id: int
    name: str
    display_name: str
    banned: bool
    published: str
    actor_id: str
    local: bool
    deleted: bool
    admin: bool
    bot_account: bool
    instance_id: int
    avatar: str | None = None
    ban_expires: str | None = None
    banner: str | None = None
    bio: str | None = None
    matrix_user_id: str | None = None
    updated: str | None = None
