import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

from django.test import Client
from accounts.models import CustomUser

c = Client()
user = CustomUser.objects.filter(is_superuser=True).first()
if user:
    c.force_login(user)
    response = c.get('/categorias/nova/')
    print("GET /categorias/nova/ status:", response.status_code)
    try:
        if response.status_code == 500:
            print("Response:", response.content)
    except Exception:
        pass
else:
    print("No superuser found")
