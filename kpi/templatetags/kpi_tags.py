from django import template
from kpi.models import Kpi

register = template.Library()


@register.simple_tag()
def get_list_kpi():
    return Kpi.objects.all()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)
