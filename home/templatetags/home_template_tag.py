from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='times')
def times(number):
    return range(number)


@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')

@register.filter
def lower(value):
    return value.lower()

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter(is_safe=False)
def c_minus(value, arg):
    """Adds the arg to the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return ''
