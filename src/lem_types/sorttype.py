"""SortType Class"""
from enum import Enum


class SortType(Enum):
    """SortType enum class."""
    Active = "Active"
    Hot = "Hot"
    New = "New"
    Old = "Old"
    TopDay = "TopDay"
    TopWeek = "TopWeek"
    TopMonth = "TopMonth"
    TopYear = "TopYear"
    TopAll = "TopAll"
    MostComments = "MostComments"
    NewComments = "NewComments"
    TopHour = "TopHour"
    TopSixHour = "TopSixHour"
    TopTwelveHour = "TopTwelveHour"
    TopThreeMonths = "TopThreeMonths"
    TopSixMonths = "TopSixMonths"
    TopNineMonths = "TopNineMonths"