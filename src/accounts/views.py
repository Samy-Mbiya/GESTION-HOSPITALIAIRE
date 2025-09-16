from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import RegisterForm, RoleUpdateForm, UserUpdateForm
from .models import Utilisateur
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from facture.models import Client


#Enregistrement de l'utilisateur
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# Modifier rôle utilisateur
@login_required
def modifier_utilisateur(request, user_id):
    #print("→ Vue appelée avec user_id =", user_id)
    if not request.user.is_superuser:
        return redirect('profil')
    user = get_object_or_404(User, id=user_id)
    utilisateur = get_object_or_404(Utilisateur, id=user_id)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        form = RoleUpdateForm(request.POST, instance=utilisateur)
        if form.is_valid() and user_form.is_valid() :
            user_form.save()
            form.save()
            messages.success(request, "Informations mises à jour avec succès.")
            return redirect('profil')
    else:
        user_form = UserUpdateForm(instance=user)
        form = RoleUpdateForm(instance=utilisateur)

    return render(request, 'accounts/modifier_utilisateur.html', {'form': form, 'user_form': user_form, 'utilisateur': utilisateur})

# Supprimer un utilisateur
@login_required
def supprimer_utilisateur(request, user_id):
    if not request.user.is_superuser: #si ce n'est pas un super utilisateur
        return redirect('profil')

    utilisateur = get_object_or_404(Utilisateur, id=user_id)

    if request.method == 'POST':
        utilisateur.user.delete()  # Supprime l'objet User lié
        messages.success(request, "Utilisateur supprimé avec succès.")
        return redirect('profil')

    return render(request, 'accounts/supprimer_utilisateur.html', {'utilisateur': utilisateur})

#Affichage du profil d'utilisateur
@login_required
def profil(request):
    utilisateur = Utilisateur.objects.get(user=request.user)

    if request.user.is_superuser:
        # Vue admin : liste des utilisateurs
        utilisateurs = Utilisateur.objects.select_related('user').exclude(user__is_superuser=True)
        return render(request, 'accounts/profil_admin.html', {'utilisateurs': utilisateurs})

    elif utilisateur.role == 'manager':
        # Vue manager : liste des clients
        clients = Client.objects.all('user')
        return render(request, 'client/liste_client.html', {'clients': clients})

    else:
        # Vue utilisateur normal : ses propres clients
        clients = Client.objects.all()
        return render(request, 'client/liste_client.html', {'clients': clients})
#Deconnection
def logout_view(request):
    logout(request)
    return redirect('login')  # ou autre nom d'URL après déconnexion