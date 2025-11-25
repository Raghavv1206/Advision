# backend/core/utils/timezone_utils.py
"""
Timezone utility functions for AdVision project.
Always use these instead of datetime.datetime directly to avoid timezone warnings.

Usage:
    from core.utils.timezone_utils import now, today, days_ago
    
    current_time = now()           # Instead of datetime.now()
    today_date = today()           # Instead of datetime.now().date()
    week_ago = days_ago(7)         # Instead of date - timedelta(days=7)
"""

from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta, date, time
import pytz


def now():
    """
    Get current timezone-aware datetime.
    
    Returns:
        datetime: Current datetime with timezone info
    
    Example:
        >>> from core.utils.timezone_utils import now
        >>> current_time = now()
        >>> print(current_time)
        2025-11-22 19:30:00+00:00
    """
    return timezone.now()


def today():
    """
    Get today's date.
    
    Returns:
        date: Today's date
    
    Example:
        >>> from core.utils.timezone_utils import today
        >>> today_date = today()
        >>> print(today_date)
        2025-11-22
    """
    return timezone.now().date()


def make_aware(dt, tz=None):
    """
    Convert naive datetime to timezone-aware datetime.
    
    Args:
        dt (datetime): Naive datetime to convert
        tz (timezone, optional): Target timezone. Defaults to settings.TIME_ZONE
    
    Returns:
        datetime: Timezone-aware datetime
    
    Example:
        >>> from core.utils.timezone_utils import make_aware
        >>> from datetime import datetime
        >>> naive_dt = datetime(2025, 11, 22, 10, 30)
        >>> aware_dt = make_aware(naive_dt)
        >>> print(aware_dt)
        2025-11-22 10:30:00+00:00
    """
    if timezone.is_aware(dt):
        return dt
    return timezone.make_aware(dt, timezone=tz)


def make_naive(dt, tz=None):
    """
    Convert timezone-aware datetime to naive datetime.
    
    Args:
        dt (datetime): Timezone-aware datetime
        tz (timezone, optional): Target timezone. Defaults to settings.TIME_ZONE
    
    Returns:
        datetime: Naive datetime
    
    Example:
        >>> from core.utils.timezone_utils import make_naive, now
        >>> aware_dt = now()
        >>> naive_dt = make_naive(aware_dt)
        >>> print(naive_dt)
        2025-11-22 10:30:00
    """
    if timezone.is_naive(dt):
        return dt
    return timezone.make_naive(dt, timezone=tz)


def start_of_day(dt=None):
    """
    Get start of day (00:00:00) for given date.
    
    Args:
        dt (datetime or date, optional): Date to get start of. Defaults to today
    
    Returns:
        datetime: Timezone-aware datetime at 00:00:00
    
    Example:
        >>> from core.utils.timezone_utils import start_of_day
        >>> day_start = start_of_day()
        >>> print(day_start)
        2025-11-22 00:00:00+00:00
    """
    if dt is None:
        dt = today()
    elif isinstance(dt, datetime):
        dt = dt.date()
    
    return make_aware(datetime.combine(dt, time.min))


def end_of_day(dt=None):
    """
    Get end of day (23:59:59.999999) for given date.
    
    Args:
        dt (datetime or date, optional): Date to get end of. Defaults to today
    
    Returns:
        datetime: Timezone-aware datetime at 23:59:59
    
    Example:
        >>> from core.utils.timezone_utils import end_of_day
        >>> day_end = end_of_day()
        >>> print(day_end)
        2025-11-22 23:59:59.999999+00:00
    """
    if dt is None:
        dt = today()
    elif isinstance(dt, datetime):
        dt = dt.date()
    
    return make_aware(datetime.combine(dt, time.max))


def days_ago(days):
    """
    Get date N days ago from today.
    
    Args:
        days (int): Number of days ago
    
    Returns:
        date: Date N days ago
    
    Example:
        >>> from core.utils.timezone_utils import days_ago
        >>> week_ago = days_ago(7)
        >>> print(week_ago)
        2025-11-15
    """
    return today() - timedelta(days=days)


def days_from_now(days):
    """
    Get date N days from today.
    
    Args:
        days (int): Number of days from now
    
    Returns:
        date: Date N days from now
    
    Example:
        >>> from core.utils.timezone_utils import days_from_now
        >>> next_week = days_from_now(7)
        >>> print(next_week)
        2025-11-29
    """
    return today() + timedelta(days=days)


def datetime_ago(days=0, hours=0, minutes=0, seconds=0):
    """
    Get timezone-aware datetime in the past.
    
    Args:
        days (int): Days ago
        hours (int): Hours ago
        minutes (int): Minutes ago
        seconds (int): Seconds ago
    
    Returns:
        datetime: Timezone-aware datetime in the past
    
    Example:
        >>> from core.utils.timezone_utils import datetime_ago
        >>> two_hours_ago = datetime_ago(hours=2)
        >>> print(two_hours_ago)
        2025-11-22 17:30:00+00:00
    """
    return now() - timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


def datetime_from_now(days=0, hours=0, minutes=0, seconds=0):
    """
    Get timezone-aware datetime in the future.
    
    Args:
        days (int): Days from now
        hours (int): Hours from now
        minutes (int): Minutes from now
        seconds (int): Seconds from now
    
    Returns:
        datetime: Timezone-aware datetime in the future
    
    Example:
        >>> from core.utils.timezone_utils import datetime_from_now
        >>> in_two_days = datetime_from_now(days=2)
        >>> print(in_two_days)
        2025-11-24 19:30:00+00:00
    """
    return now() + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


def parse_date_string(date_string, format='%Y-%m-%d'):
    """
    Parse date string to timezone-aware datetime.
    
    Args:
        date_string (str): Date string to parse
        format (str): Date format. Defaults to '%Y-%m-%d'
    
    Returns:
        datetime: Timezone-aware datetime
    
    Example:
        >>> from core.utils.timezone_utils import parse_date_string
        >>> dt = parse_date_string('2025-11-22')
        >>> print(dt)
        2025-11-22 00:00:00+00:00
    """
    naive_dt = datetime.strptime(date_string, format)
    return make_aware(naive_dt)


def format_datetime(dt, format='%Y-%m-%d %H:%M:%S'):
    """
    Format datetime to string.
    
    Args:
        dt (datetime): Datetime to format
        format (str): Output format. Defaults to '%Y-%m-%d %H:%M:%S'
    
    Returns:
        str: Formatted datetime string
    
    Example:
        >>> from core.utils.timezone_utils import now, format_datetime
        >>> current = now()
        >>> formatted = format_datetime(current)
        >>> print(formatted)
        '2025-11-22 19:30:00'
    """
    return dt.strftime(format)


def is_past(dt):
    """
    Check if datetime/date is in the past.
    
    Args:
        dt (datetime or date): Datetime or date to check
    
    Returns:
        bool: True if in the past, False otherwise
    
    Example:
        >>> from core.utils.timezone_utils import is_past, days_ago
        >>> yesterday = days_ago(1)
        >>> print(is_past(yesterday))
        True
    """
    if isinstance(dt, date) and not isinstance(dt, datetime):
        return dt < today()
    if timezone.is_naive(dt):
        dt = make_aware(dt)
    return dt < now()


def is_future(dt):
    """
    Check if datetime/date is in the future.
    
    Args:
        dt (datetime or date): Datetime or date to check
    
    Returns:
        bool: True if in the future, False otherwise
    
    Example:
        >>> from core.utils.timezone_utils import is_future, days_from_now
        >>> tomorrow = days_from_now(1)
        >>> print(is_future(tomorrow))
        True
    """
    if isinstance(dt, date) and not isinstance(dt, datetime):
        return dt > today()
    if timezone.is_naive(dt):
        dt = make_aware(dt)
    return dt > now()


def get_user_timezone(user):
    """
    Get user's timezone preference.
    
    Args:
        user (User): User object
    
    Returns:
        timezone: User's timezone or default
    
    Note:
        Extend User model with 'timezone' field to enable per-user timezones
    
    Example:
        >>> from core.utils.timezone_utils import get_user_timezone
        >>> user_tz = get_user_timezone(request.user)
    """
    # If you add timezone field to User model:
    # if hasattr(user, 'timezone') and user.timezone:
    #     return pytz.timezone(user.timezone)
    
    return timezone.get_default_timezone()


def convert_to_user_timezone(dt, user):
    """
    Convert datetime to user's timezone.
    
    Args:
        dt (datetime): Datetime to convert
        user (User): User object
    
    Returns:
        datetime: Datetime in user's timezone
    
    Example:
        >>> from core.utils.timezone_utils import convert_to_user_timezone
        >>> user_time = convert_to_user_timezone(now(), request.user)
    """
    user_tz = get_user_timezone(user)
    if timezone.is_naive(dt):
        dt = make_aware(dt)
    return dt.astimezone(user_tz)


# Quick access for common operations
get_current_time = now
get_today = today
get_start_of_day = start_of_day
get_end_of_day = end_of_day