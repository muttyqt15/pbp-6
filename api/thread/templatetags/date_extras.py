from django.utils import timezone
from datetime import datetime, timedelta
from django import template

register = template.Library()

@register.filter
def time_ago(dt):
    # Check if the provided datetime is naive
    if dt.tzinfo is None:
        # If it's naive, make it aware using the current timezone
        dt = timezone.make_aware(dt)

    # Get the current time
    now = timezone.now()

    # Calculate the difference
    delta = now - dt

    # Define the time thresholds
    if delta < timedelta(seconds=60):
        return f"{int(delta.total_seconds())} seconds ago"
    elif delta < timedelta(minutes=60):
        return f"{delta.seconds // 60} minutes ago"
    elif delta < timedelta(hours=24):
        return f"{delta.seconds // 3600} hours ago"
    else:
        days = delta.days
        return f"{days} day{'s' if days > 1 else ''} ago"
