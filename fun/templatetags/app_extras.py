from django import template

register = template.Library()


@register.filter
def blue(value, arg):
    """Returns string in HTML blue"""
    return value.replace(arg, '<span style="color: blue">' + arg + '</span>')


@register.filter
def tile(value):
    """Returns what class of tile needs to be rendered for numberdle"""
    if '=' in value:
        return 'tile--correct'
    else:
        return 'tile--incorrect'


@register.filter
def hint(value):
    """Returns what hint needs to be provided for numberdle"""
    if '=' in value:
        return ' class="hint--success" aria-label="Correct!"'
    elif '>' in value:
        return ' class="hint--info" aria-label="Input Number > Hidden Number"'
    elif '<' in value:
        return ' class="hint--info" aria-label="Input Number < Hidden Number"'
    else:
        return ' '
