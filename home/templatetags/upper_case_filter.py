from django import template

register = template.Library()


@register.filter()
def convert_to_upper_case(value):
    return value.capitalize()
