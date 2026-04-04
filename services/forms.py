from django import forms
from .models import ServiceOffer, ServiceRequest

class ServiceOfferForm(forms.ModelForm):
    class Meta:
        model = ServiceOffer
        fields = ['category', 'title', 'description', 'price_base']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Ex: Pintor profissional em domicílio'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Descreva detalhadamente seu serviço...'
            }),
            'category': forms.Select(attrs={
                'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500'
            }),
            'price_base': forms.NumberInput(attrs={
                'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
                'placeholder': '0.00'
            }),
        }

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['category', 'title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500',
                'placeholder': 'Ex: Preciso de limpeza pesada pós-obra'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500',
                'placeholder': 'Descreva o que você precisa e quando...'
            }),
            'category': forms.Select(attrs={
                'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500'
            }),
        }
