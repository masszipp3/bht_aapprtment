from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def mul(value, arg):
    return round(value * arg,3)

@register.filter
def sub(value, arg):
    return round(value - arg,3)

@register.filter
def abs(value):
    """Returns the absolute value of the argument."""
    return abs(value)

@register.filter
def calculate_sgst(value, rate=9):
    try:
        return round(Decimal(value) * Decimal(rate) / 100, 3)
    except (TypeError, ValueError, InvalidOperation):
        return 0

@register.filter
def calculate_cgst(value, rate=9):
    try:
        return round(Decimal(value) * Decimal(rate) / 100, 3)
    except (TypeError, ValueError, InvalidOperation):
        return 0
