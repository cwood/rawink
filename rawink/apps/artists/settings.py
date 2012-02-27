from django.conf import settings

_app_settings = getattr(settings, 'ARTISTS', None) or {}
ARTIST_GROUP = _app_settings.get('ARTIST_GROUP') or 'artist'