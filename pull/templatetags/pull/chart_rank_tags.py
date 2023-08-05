from django import template

register = template.Library()

def split_and_capitalize(value, delim=" "):
    words = [word.upper() if word =="dci" else word.capitalize() for word in value.split(delim)]
    return " ".join(words)

register.filter("SAC", split_and_capitalize)
