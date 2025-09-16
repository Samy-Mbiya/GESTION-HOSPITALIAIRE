from django.urls import path

from .views import registerClient, editteClient, supprimerClient, recherche

urlpatterns=[
    path('registerclient/', registerClient, name='registerclient'), #Enregistrement
    path('',recherche,name='liste-recheClient'),#Recherche
    path('editclient/<int:client_id>/',editteClient,name='editclient'),#Modification
    path('suppclient/<int:client_id>/',supprimerClient,name='suppclient'),#Suppression
    #path('', listeClient, name='listeclient' ),#Affichage

]