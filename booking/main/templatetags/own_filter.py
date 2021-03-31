from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def string_reverse(value):
    reverse = []
    length = len(value)
    for i in range(length):
        reverse.append(value[length - i - 1])
    return ''.join(reverse)
