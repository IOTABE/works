from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm, ClientProfileForm, ProfessionalProfileForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    if user.is_professional:
        profile = user.professional_profile
        profile_form_class = ProfessionalProfileForm
    elif user.is_client:
        profile = user.client_profile
        profile_form_class = ClientProfileForm
    else:
        # Create a default client profile if missing (e.g., for superusers)
        from .models import ClientProfile
        profile, created = ClientProfile.objects.get_or_create(user=user)
        profile_form_class = ClientProfileForm

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = profile_form_class(request.POST, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = profile_form_class(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)
