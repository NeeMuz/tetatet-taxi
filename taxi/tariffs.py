"""Каталог тарифов и типов поездок."""
from decimal import Decimal

TARIFF_CATALOG = {
    'economy': {
        'label': 'Эконом',
        'display': 'Economy',
        'icon': '🚗',
        'multiplier': Decimal('1.00'),
        'eta_offset': -2,
        'meta': '4 места',
        'example_car': 'VW Golf',
        'category': 'standard',
        'desc': 'Быстрая поездка по городу',
    },
    'comfort': {
        'label': 'Комфорт',
        'display': 'Comfort',
        'icon': '🚙',
        'multiplier': Decimal('1.40'),
        'eta_offset': 1,
        'meta': '4 места · просторнее',
        'example_car': 'Toyota Camry',
        'category': 'standard',
        'desc': 'Больше места и тишина в салоне',
    },
    'business': {
        'label': 'Бизнес',
        'display': 'Business',
        'icon': '✨',
        'multiplier': Decimal('1.85'),
        'eta_offset': 3,
        'meta': 'премиум-класс',
        'example_car': 'Mercedes E-class',
        'category': 'standard',
        'desc': 'Премиум-авто и приоритет',
    },
    'minivan': {
        'label': 'Минивэн',
        'display': 'Minivan',
        'icon': '🚐',
        'multiplier': Decimal('2.25'),
        'eta_offset': 4,
        'meta': '6–7 мест · просторно',
        'example_car': 'Mercedes V-class',
        'category': 'standard',
        'desc': 'Больше места для компании и багажа',
    },
    'cargo': {
        'label': 'Грузовой',
        'display': 'Cargo',
        'icon': '🚚',
        'multiplier': Decimal('2.10'),
        'eta_offset': 6,
        'meta': 'до 800 кг',
        'example_car': 'Ford Transit',
        'category': 'special',
        'desc': 'Перевозка груза и крупных вещей',
    },
    'pets': {
        'label': 'С животными',
        'display': 'PetRide',
        'icon': '🐾',
        'multiplier': Decimal('1.25'),
        'eta_offset': 3,
        'meta': 'переноска · плед',
        'example_car': 'Skoda Octavia',
        'category': 'special',
        'desc': 'Водитель готов к поездке с питомцем',
    },
    'kids': {
        'label': 'С детьми',
        'display': 'Family',
        'icon': '👶',
        'multiplier': Decimal('1.15'),
        'eta_offset': 2,
        'meta': 'детское кресло',
        'example_car': 'VW Passat',
        'category': 'special',
        'desc': 'Кресло и спокойная поездка с ребёнком',
    },
}

TARIFF_CHOICES = [(k, v['label']) for k, v in TARIFF_CATALOG.items()]

TARIFF_MULTIPLIERS = {k: v['multiplier'] for k, v in TARIFF_CATALOG.items()}

STANDARD_TARIFFS = [k for k, v in TARIFF_CATALOG.items() if v['category'] == 'standard']
SPECIAL_TARIFFS = [k for k, v in TARIFF_CATALOG.items() if v['category'] == 'special']
