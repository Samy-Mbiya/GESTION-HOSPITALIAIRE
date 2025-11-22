from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientRegisterForm, FactureForm, NhForm, DescriptionForm, FacUpdateForm, DescriptionUpdatForm, \
    NhUpdateForm
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
    clients = Client.objects.all().order_by('-id')[:10] # affiche tout
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

# Liste, Recherche et Enregistrement de Facture Client
@login_required
def listFac(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    query = request.GET.get("rech")  # on récupère la valeur du champ "rech"
    if query:
        factures = Facture.objects.filter(date__icontains=query)  # recherche insensible à la casse
    else:
        factures = Facture.objects.filter(client=client).order_by('-date')[:10]

    # Vue principale pour créer une facture (page avec JS dynamique).
    if request.method == 'POST':
        form = FactureForm(request.POST)
        formNh = NhForm(request.POST)
        if form.is_valid():
            #Client
            facture = form.save(commit=False)
            facture.client = client  # 🔒 lie automatiquement au client
            facture.user = request.user
            facture.save()
            facture_id = facture.id  # ✅ récupère l'ID

            #Note d'Honoraire
            nh = formNh.save(commit=False)
            nh.client = client  # 🔒 lie automatiquement au client
            nh.user = request.user
            nh.save()

            return redirect('add_description', facture_id=facture_id)
    else:
        # ✅ on passe l'ID du client en valeur initiale du champ caché
        form = FactureForm(initial={'client': client.id})

    return render(request, 'facture/liste_facture.html', {
        'form': form,
        'factures': factures,
        'client': client,
    })

# Modification de la Facture Client
@login_required
def updateFac(request,facture_id):
    facture = get_object_or_404(Facture, id=facture_id)

    if request.method == 'POST':
        form = FacUpdateForm(request.POST, instance=facture)
        if form.is_valid():
            facture = form.save(commit=False)
            facture.user = request.user  # Facultatif : met à jour l'utilisateur qui modifie
            facture.save()
            facture.update_totals()  # 🔁 Recalcule les totaux après modif
            #messages.success(request, "✅ La facture a été mise à jour avec succès.")
            return redirect('add_description', facture_id=facture.id)  # Redirige vers le détail (à adapter)
        #else:
            #messages.error(request, "⚠️ Une erreur est survenue. Vérifie les champs.")
    else:
        form = FacUpdateForm(instance=facture)

    return render(request, 'facture/modification_facture.html', {
        'form': form,
        'facture': facture
    })

# Suppression de la Facture
@login_required
def deleteFac(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)  # Récupération de la facture
    client_id = facture.client.id  # On récupère l'ID avant de supprimer la facture

    if request.method == 'POST':
        facture.delete()  # Suppression
        return redirect('list_Fac', client_id=client_id)  # ✅ redirection correcte
    return render(request, 'facture/supprimer_facture.html', {'facture': facture})


# ================== DESCRIPTION POUR FACTURE ==================
#Enregistrement Description
#---------------------------
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
    #Facture Mise à jour de
    descriptions = Description.objects.filter(facture=facture)
    total_general = descriptions.aggregate(sum_total=Sum('total'))['sum_total'] or 0

    return render(request, 'facture/description_facture.html', {
        'form': form,
        'facture': facture,
        'descriptions': descriptions,
        'type_doc': 'Facture',
        'total_general': total_general,
    })

#Modification  Description
#---------------------------
@login_required
def update_Description(request, description_id):
    description = get_object_or_404(Description, id=description_id)

    if request.method == 'POST':
        form = DescriptionUpdatForm(request.POST, instance=description) #Remplissage du formileur

        if form.is_valid():
            description = form.save(commit=False)
            description.save()
            return redirect('add_description', facture_id=description.facture.id)
        else:
            print(form.errors)

    else:
        form = DescriptionUpdatForm(instance=description)

    return render(request, 'facture/modification_description.html', {
        'form': form,
        'description': description,
    })

# Suppression de la Description
@login_required
def deleteDesc(request, description_id):
    description = get_object_or_404(Description, id=description_id)  # Récupération de la facture
    facture_id=description.facture.id
    if request.method == 'POST':
        description.delete()  # Suppression
        return redirect('add_description', facture_id=facture_id)  # ✅ redirection correcte
    return render(request, 'facture/supprimer_description.html', {'description': description, 'facture_id':facture_id})


# ========================NOTE D'HONORAIRE=================================================
#Liste Honoraire par client
@login_required
def listHon(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    query = request.GET.get("rech")  # on récupère la valeur du champ "rech"
    if query:
        honoraires = Nh.objects.filter(date__icontains=query)  # recherche insensible à la casse
    else:
        honoraires = Nh.objects.filter(client=client).order_by('-date')[:10]

    return render(request, 'honoraire/liste_honoraire.html', {
        'honoraires': honoraires,
        'client': client,
    })

# Modification de la NH
@login_required
def updateNh(request,honoraire_id):
    honoraire = get_object_or_404(Nh, id=honoraire_id)

    if request.method == 'POST':
        form = NhUpdateForm(request.POST, instance=honoraire)
        if form.is_valid():
            honoraire = form.save(commit=False)
            honoraire.user = request.user  # Facultatif : met à jour l'utilisateur qui modifie
            honoraire.save()
            honoraire.update_totals()  # 🔁 Recalcule les totaux après modif
            #messages.success(request, "✅ La facture a été mise à jour avec succès.")
            return redirect('add_description_nh', honoraire_id=honoraire.id)  # Redirige vers le détail (à adapter)
        #else:
            #messages.error(request, "⚠️ Une erreur est survenue. Vérifie les champs.")
    else:
        form = NhUpdateForm(instance=honoraire)

    return render(request, 'honoraire/modification_honoraire.html', {
        'form': form,
        'honoraire': honoraire
    })


# ================== DESCRIPTION POUR HONORAIRE ==================
@login_required
def add_description_nh(request, honoraire_id):
    nh = get_object_or_404(Nh, pk=honoraire_id)
    if request.method == 'POST':
        form = DescriptionForm(request.POST)
        if form.is_valid():
            description = form.save(commit=False)
            description.nh = nh
            description.save()
            return redirect('add_description_nh', honoraire_id=honoraire_id)
    else:
        form = DescriptionForm()

        # Facture Mise à jour de
    descriptions = Description.objects.filter(nh=nh)
    total_general = descriptions.aggregate(sum_total=Sum('total'))['sum_total'] or 0
    return render(request, 'honoraire/description_honoraire.html', {
        'form': form,
        'nh': nh,
        'descriptions': descriptions,
        'type_doc': 'NH'
    })