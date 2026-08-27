"""Хелперы локализации для views, API и каталога тарифов."""

from .translations import TRANSLATIONS, translate
from taxi.tariffs import TARIFF_CATALOG


def translated_tariff_catalog(lang: str) -> dict:
    catalog = {}
    for key, info in TARIFF_CATALOG.items():
        catalog[key] = {
            **info,
            'label': translate(f'tariff.{key}.label', lang),
            'display': translate(f'tariff.{key}.display', lang),
            'meta': translate(f'tariff.{key}.meta', lang),
            'desc': translate(f'tariff.{key}.desc', lang),
        }
    return catalog


def tariff_label(tariff: str, lang: str = 'ru') -> str:
    return translate(f'tariff.{tariff}.label', lang) if tariff else ''


def status_label(status: str, lang: str = 'ru') -> str:
    return translate(f'status.{status}', lang) if status else ''


def all_js_translations(lang: str) -> dict:
    return {key.replace('.', '_'): translate(key, lang) for key in TRANSLATIONS}
