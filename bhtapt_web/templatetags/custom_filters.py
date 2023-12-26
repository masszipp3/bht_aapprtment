from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def mul(value, arg):
    return round(value * arg,3)

@register.filter
def sub(value, arg):
    return round(value - arg,3)
