from django.template.loader_tags import register
from django.template import loader, Context, defaultfilters, TemplateDoesNotExist

import markdown


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


@register.simple_tag(takes_context=True)
def include_md(context, template_name):
    lang = context['LANGUAGE_CODE'].replace('-', '_')
    try:
        t = loader.render_to_string('markdown/{}/{}'.format(lang, template_name), context)
    except TemplateDoesNotExist:
        t = loader.render_to_string('markdown/en_US/{}'.format(template_name), context)

    html = markdown.markdown(t)

    return defaultfilters.safe(html)
