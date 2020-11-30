import bleach

from django import template
from django.utils.safestring import mark_safe

SETTINGS = {
    "strip": True,
    "strip_comments": True,
}


def strip_all_tags(value):
    """Strip all tags"""
    bleached_value = bleach.clean(value, **SETTINGS)
    return mark_safe(bleached_value)


register = template.Library()
register.filter("bleach_all", strip_all_tags)
