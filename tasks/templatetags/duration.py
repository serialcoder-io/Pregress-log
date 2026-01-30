from django import template

register = template.Library()

@register.filter
def duration(value):
    if value is None:
        return ""

    try:
        minutes = int(value)
    except (TypeError, ValueError):
        return ""

    hours = minutes // 60
    remaining = minutes % 60

    if hours == 0:
        return f"{remaining} mn"

    if remaining == 0:
        return f"{hours}h"

    return f"{hours}h {remaining}mn"
