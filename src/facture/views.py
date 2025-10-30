from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientRegisterForm, FactureForm, NhForm, DescriptionForm
from .models import Client, Facture, Nh, Description


# CLIENT
#--------
#Detail Client
@login_required
def detailClient(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'client/detail_client.html', {'client': client})

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
        return redirect('liste-recheClient')
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
            return redirect('liste-recheClient')  # Ou la page où tu veux retourner
    else:
        form = ClientRegisterForm(instance=client)

    return render(request, 'client/modification_client.html', {'form': form, 'client': client})

#Suppresiont de client
@login_required
def supprimerClient(request, client_id):

    if not request.user.is_superuser: #si ce n'est pas un super utilisateur
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer ce client.")

    client = get_object_or_404(Client, id=client_id) # recuperation de l'ID dans la table Client
    if request.method == 'POST':
        client.delete()  # Supprime client lié
        return redirect('liste-recheClient')

    return render(request, 'client/supprimer_client.html', {'client': client})


# ========================FACTURE=================================================

# Liste et Enregistrement de Facture Client
def listFac(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    factures = Facture.objects.filter(client=client).order_by('-date')
    # Vue principale pour créer une facture (page avec JS dynamique).
    if request.method == 'POST':
        form = FactureForm(request.POST)
        # formset = DescriptionForm(request.POST)
        if form.is_valid():
            facture = form.save(commit=False)
            facture.client = client  # 🔒 lie automatiquement au client
            facture.user = request.user
            facture.save()
            facture_id = facture.id  # ✅ récupère l'ID
            return redirect('add_description', facture_id=facture_id)
    else:
        # ✅ on passe l'ID du client en valeur initiale du champ caché
        form = FactureForm(initial={'client': client.id})

    return render(request, 'facture/liste_facture.html', {
        'form': form,
        'factures': factures,
        'client': client,
    })

# ================== DESCRIPTION POUR FACTURE ==================
@login_required
def add_description(request, facture_id):
    facture = get_object_or_404(Facture, pk=facture_id)
    if request.method == 'POST':
        form = DescriptionForm(request.POST)
        if form.is_valid():
            description = form.save(commit=False)
            description.facture = facture
            description.save()  # ✅ Sauvegarde effective
            return redirect('add_description', facture_id=facture.id)
        else:
            print(form.errors)  # 🔍 Pour voir les erreurs dans la console
    else:
        form = DescriptionForm()

    descriptions = Description.objects.filter(facture=facture)
    total_general = descriptions.aggregate(sum_total=Sum('total'))['sum_total'] or 0
    return render(request, 'facture/description_facture.html', {
        'form': form,
        'facture': facture,
        'descriptions': descriptions,
        'type_doc': 'Facture',
        'total_general': total_general,
    })



# HONORAIRE
#-----------
#Liste Honoraire par client
def listHon(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    nhs = Nh.objects.filter(client=client)
    return render(request, "honoraire/liste_honoraire.html", {
        "client": client,
        "nhs": nhs,
    })

# Enregistrement Honoraire
@login_required
def create_nh(request):
    if request.method == 'POST':
        form = NhForm(request.POST)
        if form.is_valid():
            nh = form.save(commit=False)
            nh.user = request.user
            nh.save()
            return redirect('add_description_nh', nh_id=nh.id)
    else:
        form = NhForm()

    last_nh = Nh.objects.last()
    next_id = (last_nh.id + 1) if last_nh else 1
    return render(request, 'honoraire/register_honoraire.html', {'form': form, 'next_id': next_id})



# ================== DESCRIPTION POUR HONORAIRE ==================
@login_required
def add_description_nh(request, nh_id):
    nh = get_object_or_404(Nh, pk=nh_id)
    if request.method == 'POST':
        form = DescriptionForm(request.POST)
        if form.is_valid():
            description = form.save(commit=False)
            description.nh = nh
            description.save()
            return redirect('add_description_nh', nh_id=nh.id)
    else:
        form = DescriptionForm()

    descriptions = nh.description_set.all()
    return render(request, 'app/description_form.html', {
        'form': form,
        'document': nh,
        'descriptions': descriptions,
        'type_doc': 'NH'
    })