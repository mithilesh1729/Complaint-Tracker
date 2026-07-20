from django.utils.timesince import timesince
from django.utils.timezone import now


def humanize_datetime(dt):
    if not dt:
        return "-"

    return f"{timesince(dt, now())} ago"