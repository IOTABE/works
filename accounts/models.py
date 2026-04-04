from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    @property
    def is_client(self):
        return hasattr(self, 'client_profile')

    @property
    def is_professional(self):
        return hasattr(self, 'professional_profile')

class ClientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_profile')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço")

    def __str__(self):
        return f"Cliente: {self.user.username}"

class ProfessionalProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='professional_profile')
    bio = models.TextField(blank=True, null=True, verbose_name="Biografia")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone Profissional")
    
    def __str__(self):
        return f"Profissional: {self.user.username}"
