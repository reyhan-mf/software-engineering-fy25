from datetime import datetime

def parse_datetime(date_str):
    """Parse a datetime string into a datetime object."""
    formats = [
        '%Y-%m-%d %H:%M:%S',  # 2023-01-01 15:00:00
        '%Y-%m-%d',           # 2023-01-01
        '%Y-%m-%dT%H:%M:%S',  # 2023-01-01T15:00:00
        '%Y-%m-%dT%H:%M:%S.%f',  # 2023-01-01T15:00:00.000
        '%Y-%m-%dT%H:%M:%SZ'  # 2023-01-01T15:00:00Z
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
            
    raise ValueError(
        f"Invalid date format: {date_str}. "
        "Supported formats are: YYYY-MM-DD, YYYY-MM-DD HH:MM:SS, "
        "YYYY-MM-DDThh:mm:ss, YYYY-MM-DDThh:mm:ss.sss"
    )