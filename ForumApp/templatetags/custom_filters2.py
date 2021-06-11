from django import template

register = template.Library()


def range_filter2(value):
    return value[0:200] + "......."


register.filter('range_filter2', range_filter2)
