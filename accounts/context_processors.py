from django.conf import settings

import json

from tetatet.translations import LANGUAGES, js_translations, resolve_language


def site_settings(request):
    lang = resolve_language(request)
    return {
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
        'CURRENT_LANGUAGE': lang,
        'LANGUAGES': LANGUAGES,
        'TETATET_JS_I18N': json.dumps(js_translations(lang), ensure_ascii=False),
    }
