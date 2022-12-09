from django import template

register = template.Library()


@register.filter
def black(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '<span style="color: black">' + arg + '</span>')
