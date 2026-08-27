"""Профили водителей диспетчерской — рейтинг и авто."""

DRIVER_PROFILES = {
    'Klaus M.': {'rating': 4.95, 'trips': 1842, 'car': 'Mercedes E-class', 'plate': 'B-TX 421'},
    'Anna S.': {'rating': 4.88, 'trips': 1260, 'car': 'VW Passat', 'plate': 'B-TX 118'},
    'Thomas B.': {'rating': 4.72, 'trips': 890, 'car': 'Skoda Octavia', 'plate': 'B-TX 903'},
    'Maria K.': {'rating': 4.91, 'trips': 2104, 'car': 'BMW 5 Series', 'plate': 'B-TX 556'},
    'Stefan R.': {'rating': 4.83, 'trips': 1540, 'car': 'Audi A6', 'plate': 'B-TX 772'},
}

DEFAULT_PROFILE = {
    'rating': 4.80,
    'trips': 500,
    'car': 'Tetatet',
    'plate': 'B-TX •••',
}


def get_driver_profile(name: str) -> dict:
    if not name:
        return {**DEFAULT_PROFILE, 'name': ''}
    profile = DRIVER_PROFILES.get(name, DEFAULT_PROFILE)
    return {'name': name, **profile}
