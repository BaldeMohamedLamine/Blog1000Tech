from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#Inscription de l'utilisateur
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})

#Connection de User
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue, {username} !')
                return redirect('article_list')
            else:
                messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

#Deconnection de User 
def logout_view(request):
    logout(request)
    messages.success(request, 'Vous êtes déconnecté.')
    return redirect('login')

#=======================profil=================================================
@login_required
def edit_profile(request):
    # Vérifie si le profil de l'utilisateur existe, sinon, le crée
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profil')  # Redirige vers la page de profil après modification
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'account/edit_profile.html', {'form': form})


@receiver(post_save, sender=User)
@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

@login_required
def profile(request):
    return render(request, 'account/profil.html', {'user': request.user})

