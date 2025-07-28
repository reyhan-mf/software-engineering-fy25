from datetime import datetime

def parse_datetime(date_str):
    """Parse a datetime string into a datetime object."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected format is 'YYYY-MM-DD HH:MM:SS'.")