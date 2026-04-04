from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ClientProfile, ProfessionalProfile

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('client', 'Sou Cliente (Quero contratar serviços)'),
        ('professional', 'Sou Profissional (Quero oferecer serviços)'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, label="Como deseja usar a plataforma?")
    phone = forms.CharField(max_length=20, required=False, label="Telefone")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            role = self.cleaned_data.get('role')
            phone = self.cleaned_data.get('phone')
            
            if role == 'client':
                ClientProfile.objects.create(user=user, phone=phone)
            else:
                ProfessionalProfile.objects.create(user=user, phone=phone)
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'}),
            'last_name': forms.TextInput(attrs={'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'}),
            'email': forms.EmailInput(attrs={'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'}),
        }

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'}),
            'address': forms.TextInput(attrs={'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'}),
        }

class ProfessionalProfileForm(forms.ModelForm):
    class Meta:
        model = ProfessionalProfile
        fields = ['phone', 'bio']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'}),
        }
