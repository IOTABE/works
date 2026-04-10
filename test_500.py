import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from accounts.models import CustomUser

c = Client()
user = CustomUser.objects.filter(is_superuser=True).first()
if user:
    c.force_login(user)
    response = c.get('/categorias/')
    print("GET /categorias/ status:", response.status_code)
    try:
        if response.status_code == 500:
            print("Response:", response.content)
    except Exception as e:
        pass
    
    response2 = c.get('/')
    print("GET / status:", response2.status_code)
else:
    print("No superuser found")
