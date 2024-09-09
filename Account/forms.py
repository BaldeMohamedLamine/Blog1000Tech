from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Adresse e-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['biographie', 'profile_photo']
        widgets = {
            'biographie': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Écrivez quelque chose à propos de vous...',
                'rows': 5,
                'style': 'resize:none;'
            }),
            'profile_photo': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
        }
