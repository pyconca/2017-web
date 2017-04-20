from django.template.loader_tags import register
from django.template import Library, loader, Context


presenters = {
    'Speaker': 'presenters/speaker_presenter.html'
}
generic_template = 'presenters/object_presenter.html'


@register.simple_tag(takes_context=True)
def present(context, obj):
    model_name = type(obj).__name__
    template_name = presenters.get(model_name, generic_template)

    t = loader.get_template(template_name)
    return t.render(Context({
        'model_name': model_name,
        'obj': obj,
    }))


@register.filter
def noval(data, placeholder):
    if data:
        return data

    return placeholder
