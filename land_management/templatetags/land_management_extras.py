from django import template

register = template.Library()

@register.filter
def get_filename(value):
    """Returns the filename from a file path"""
    if value:
        return value.split('/')[-1]
    return '' 