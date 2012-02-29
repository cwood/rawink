from django.conf import settings

_app_settings = getattr(settings, 'CUSTOMERS', None) or {}
CUSTOMER_GROUP = _app_settings.get('CUSTOMER_GROUP') or 'customer'