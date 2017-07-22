from django import template
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag
def bilingual(obj, field, attr=None):
    """ This is a quick and dirty way to define bilingual content in a single field. """

    field_locale = '%s_%s' % (field, get_language())

    value = None
    try:
        value = getattr(obj, field_locale)
    except AttributeError:
        pass

    if not value:
        try:
            value = getattr(obj, '%s_en' % field, None)
        except AttributeError:
            pass

    if value and attr:
        try:
            return getattr(value, attr, '')
        except ValueError:
            pass

    return value or ''
