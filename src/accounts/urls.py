from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import  profil, register, logout_view, supprimer_utilisateur, modifier_utilisateur

urlpatterns = [
    path('register/', register, name='register'), #Enregistrement
    path('', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'), #Login
    path('logout/', logout_view, name='logout'), #Logout
    path('profil/', profil, name='profil'),# Profil
    path('modifier/<int:user_id>/', modifier_utilisateur, name='modifier_utilisateur'),
    path('supprimer/<int:user_id>/', supprimer_utilisateur, name='supprimer_utilisateur'),
]