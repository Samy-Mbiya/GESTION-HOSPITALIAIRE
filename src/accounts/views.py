from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, RoleUpdateForm
from .models import Utilisateur
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#Enregistrement de l'utilisateur
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# Modifier rôle utilisateur
@login_required
def modifier_utilisateur(request, user_id):
    if not request.user.utilisateur.role == 'Admin':
        return redirect('profil')

    utilisateur = get_object_or_404(Utilisateur, id=user_id)

    if request.method == 'POST':
        form = RoleUpdateForm(request.POST, instance=utilisateur)
        if form.is_valid():
            form.save()
            messages.success(request, "Rôle mis à jour avec succès.")
            return redirect('profil')
    else:
        form = RoleUpdateForm(instance=utilisateur)

    return render(request, 'accounts/modifier_utilisateur.html', {'form': form, 'utilisateur': utilisateur})

# Supprimer un utilisateur
@login_required
def supprimer_utilisateur(request, user_id):
    if not request.user.utilisateur.role == 'Admin':
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

    if utilisateur.role == 'Admin':
        # Liste de tous les utilisateurs
        utilisateurs = Utilisateur.objects.select_related('user').all()
        return render(request, 'accounts/profil_admin.html', {'utilisateurs': utilisateurs})

    elif utilisateur.role == 'manager':
        return render(request, 'accounts/profil_manager.html')

    else:
        return render(request, 'accounts/profil_utilisateur.html')

#Deconnection
def logout_view(request):
    logout(request)
    return redirect('login')  # ou autre nom d'URL après déconnexion