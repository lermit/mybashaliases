from django import template

register = template.Library()

@register.filter
def type(value):
    return type(value)
