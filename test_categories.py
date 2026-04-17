import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from services.models import Category

c = Client()

# Create superuser
admin_user, _ = User.objects.get_or_create(username='admin_test', is_superuser=True, is_staff=True)
admin_user.set_password('adminpass')
admin_user.save()

# Create normal user
normal_user, _ = User.objects.get_or_create(username='normal_test')
normal_user.set_password('normalpass')
normal_user.save()

# Test unauthorized access
c.login(username='normal_test', password='normalpass')
response = c.get('/category/list/')
print("Normal user access to list:", response.status_code) # expecting 302 or 403 (user_passes_test redirects by default to login if no login_url specified)

# Test authorized access
c.login(username='admin_test', password='adminpass')
response = c.get('/category/list/')
print("Admin user access to list:", response.status_code) # expecting 200

# Test create category
response = c.post('/category/create/', {'name': 'Test Category', 'slug': 'test-category'})
print("Create category status:", response.status_code) # expecting 302 redirection to list
cat = Category.objects.filter(slug='test-category').first()
print("Category created:", cat.name if cat else "Failed")

# Test edit category
response = c.post(f'/category/{cat.pk}/update/', {'name': 'Updated Category', 'slug': 'updated-category'})
print("Edit category status:", response.status_code)
cat.refresh_from_db()
print("Category updated name:", cat.name)

# Test delete category
response = c.post(f'/category/{cat.pk}/delete/')
print("Delete category status:", response.status_code)
print("Category exists after delete?", Category.objects.filter(pk=cat.pk).exists())
