from django import template

from tetatet.translations import LANGUAGES, resolve_language, translate

register = template.Library()


@register.simple_tag(takes_context=True)
def t(context, key):
    request = context.get('request')
    lang = resolve_language(request) if request else 'ru'
    return translate(key, lang)


@register.simple_tag(takes_context=True)
def status_label(context, status):
    request = context.get('request')
    lang = resolve_language(request) if request else 'ru'
    return translate(f'status.{status}', lang)


@register.simple_tag(takes_context=True)
def tariff_label(context, tariff):
    request = context.get('request')
    lang = resolve_language(request) if request else 'ru'
    return translate(f'tariff.{tariff}.label', lang)


@register.simple_tag(takes_context=True)
def tf(context, key, **kwargs):
    request = context.get('request')
    lang = resolve_language(request) if request else 'ru'
    text = translate(key, lang)
    for name, value in kwargs.items():
        text = text.replace('{' + name + '}', str(value))
    return text
