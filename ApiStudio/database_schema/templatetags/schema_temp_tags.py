from django import template


register = template.Library()



@register.filter(name="getattribute")
def getattribute(value, arg):
    try:
        return value[arg]
    except KeyError:
        return None
