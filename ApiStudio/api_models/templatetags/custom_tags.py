from django import template

register = template.Library()


@register.filter
def dict_items(dictionary):
    print(dictionary)
    """Filter to get dictionary items."""
    if dictionary is None:
        return []

    return dictionary.items()



