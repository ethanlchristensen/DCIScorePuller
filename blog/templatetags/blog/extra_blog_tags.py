from django import template

register = template.Library()

def chop_200(value):
    return value[:200] + " . . ."

register.filter("200", chop_200)