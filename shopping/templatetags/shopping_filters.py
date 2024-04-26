# shopping/templatetags/shopping_filters.py
from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplies the value by the arg."""
    return value * arg
