from django.db import models
import urllib.parse
import re
from accounts.models import ClientProfile, ProfessionalProfile

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='requests')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Pedido: {self.title}"

    @property
    def whatsapp_url(self):
        phone = self.client.phone
        if not phone:
            return None
        # Limpar apenas números
        clean_phone = re.sub(r'\D', '', phone)
        # Se o número não começar com 55 (Brasil), adicionamos. 
        # (Ajuste conforme a região se necessário)
        if not clean_phone.startswith('55'):
            clean_phone = f"55{clean_phone}"
            
        message = f"Olá, vi seu pedido '{self.title}' na ComunidApp e gostaria de ajudar."
        encoded_message = urllib.parse.quote(message)
        return f"https://wa.me/{clean_phone}?text={encoded_message}"

class ServiceOffer(models.Model):
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='offers')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_base = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Oferta: {self.title}"

    @property
    def whatsapp_url(self):
        phone = self.professional.phone
        if not phone:
            return None
        # Limpar apenas números
        clean_phone = re.sub(r'\D', '', phone)
        if not clean_phone.startswith('55'):
            clean_phone = f"55{clean_phone}"
            
        message = f"Olá, vi sua oferta '{self.title}' na ComunidApp e gostaria de saber mais."
        encoded_message = urllib.parse.quote(message)
        return f"https://wa.me/{clean_phone}?text={encoded_message}"
