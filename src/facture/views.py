from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientRegisterForm
from .models import Client


#Affichage de la liste des client
"""@login_required
def listeClient(request):
    clients=Client.objects.all()
    return render(request, 'client/liste_client.html', {'client': clients})
"""
#Affiche liste et Recherche client
@login_required
def recherche(request):
    query = request.GET.get("rech")  # on récupère la valeur du champ "rech"
    clients = Client.objects.all()  # affiche tout
    if query:
        clients = Client.objects.filter(nom__icontains=query)  # recherche insensible à la casse
    return render(request, 'client/liste_client.html', {'clients': clients, 'query':query})


#Enregistrement le Client
@login_required
def registerClient(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)  # On NE sauvegarde PAS encore
            client.user = request.user# On ajoute l'utilisateur connecté
            client.save()
        return redirect('listeclient')
    else:
        form = ClientRegisterForm()
    return render(request, 'client/register_client.html', {'form': form})

#Mondification du Client
@login_required
def editteClient(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        form = ClientRegisterForm(request.POST, instance=client) #Recuperation du client et son ID
        if form.is_valid():
            client = form.save(commit=False)
            if client.user.id == request.user.id:
                client.log = request.user.username
            else:
                client.log =client.user.username+", "+ request.user.username #L'utilisateur qui modifier le client
            client.save()
            return redirect('listeclient')  # Ou la page où tu veux retourner
    else:
        form = ClientRegisterForm(instance=client)

    return render(request, 'client/modification_client.html', {'form': form, 'client': client})


#Suppresiont de client
@login_required
def supprimerClient(request, client_id):

    if not request.user.is_superuser: #si ce n'est pas un super utilisateur
        #return redirect('listeclient')
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer ce client.")

    client = get_object_or_404(Client, id=client_id) # recuperation de l'ID dans la table Client
    if request.method == 'POST':
        client.delete()  # Supprime client lié
        return redirect('listeclient')

    return render(request, 'client/supprimer_client.html', {'client': client})
