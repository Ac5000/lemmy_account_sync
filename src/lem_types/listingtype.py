"""ListingType Class"""
from enum import Enum


class ListingType(Enum):
    """ListingType enum class."""
    All = "All"
    Local = "Local"
    Subscribed = "Subscribed"