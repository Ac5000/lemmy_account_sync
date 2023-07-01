"""Community Class"""
from dataclasses import dataclass


@dataclass
class Community:
    """Community dataclass."""
    id: int
    name: str
    title: str
    description: str
    removed: bool
    published: str
    updated: str
    deleted: bool
    nsfw: bool
    actor_id: str
    local: bool
    icon: str
    banner: str
    hidden: bool
    posting_restricted_to_mods: bool
    instance_id: int