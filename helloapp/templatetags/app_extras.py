from django import template

register = template.Library()


@register.filter
def blue(value, arg):
    """Returns string in HTML blue"""
    return value.replace(arg, '<span style="color: blue">' + arg + '</span>')
