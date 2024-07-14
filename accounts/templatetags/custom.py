from django import template

register = template.Library()
counter = 0

@register.simple_tag
def counter_value():
    global counter
    current_counter = counter
    counter = counter+1
    return current_counter


@register.simple_tag
def counter_reset():
    global counter
    counter = 0
    return ""


@register.filter(name="remainder")
def result(value):
    return value%3

