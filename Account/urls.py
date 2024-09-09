from django.urls import path
from .views import register_view, login_view, logout_view
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

     path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), 
        name='password_reset'),
    
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'), 
        name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'), 
        name='password_reset_confirm'),
    
    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_done.html'), 
        name='password_reset_complete'),
    
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profil',views.profile,name='profil'),
    
]
