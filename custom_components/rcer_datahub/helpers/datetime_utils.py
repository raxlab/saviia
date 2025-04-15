from datetime import datetime
from zoneinfo import ZoneInfo


def today(timezone: str = "America/Santiago") -> str:
    """
    Return the current date.

    :param timezone: A string representing the IANA timezone name.
        Defaults to "America/Santiago".
    :return datetime:
    """
    return datetime.now(tz=ZoneInfo(timezone))


def datetime_to_str(date: datetime, date_format: str = "%Y-%m-%dT%H:%M%:S") -> str:
    """
    Convert a datetime object to a string in the specified format.

    :param date: The datetime object to convert.
    :param date_format: The format to convert the datetime object to.
        Defaults to "YYYYMMDD:HHMMSS".
    :return: A string in the specified format.
    """
    return date.strftime(date_format)
