from datetime import datetime, timezone


def generate_time() -> datetime:
    return datetime.now(timezone.utc)
