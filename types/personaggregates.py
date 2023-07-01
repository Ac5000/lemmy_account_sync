"""PersonAggregates Class"""
from dataclasses import dataclass


@dataclass
class PersonAggregates:
    """PersonAggregates dataclass."""
    id: int
    person_id: int
    post_count: int
    post_score: int
    comment_count: int
    comment_score: int