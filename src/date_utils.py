from datetime import datetime, timezone


def get_iso_datetime() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+0000")


def get_iso_date_tz() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d+0000")
