from urllib.parse import quote_plus
from django import template

register = template.Library()

@register.filter(name='urlify')
def make_url_sharable(value):
    return quote_plus(value)
