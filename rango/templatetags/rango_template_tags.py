from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/categories_tag.html')
def get_category_list(active_category = None):
    return {'categories':Category.objects.all(),
            'active_category':active_category}