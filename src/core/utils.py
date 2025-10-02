from datetime import datetime, timezone


def generate_time():
    return datetime.now(timezone.utc)
