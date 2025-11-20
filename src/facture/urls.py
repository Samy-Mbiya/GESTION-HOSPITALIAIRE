from django.urls import path

from .views import registerClient, editteClient, supprimerClient, recherche, \
    listFac, listHon, create_nh, add_description, add_description_nh, updateFac, deleteFac, update_Description, \
    deleteDesc

urlpatterns=[
    #Client
    path('registerclient/', registerClient, name='registerclient'), #Enregistrement Client
    path('',recherche,name='liste-recheClient'),#Recherche Client
    path('editclient/<int:client_id>/',editteClient,name='editclient'),#Modification Client
    path('suppclient/<int:client_id>/',supprimerClient,name='suppclient'),#Suppression Client

    #Facture
    path('list_fac/<int:client_id>/',listFac,name='list_Fac'),#Liste et enregistrement de la  Facture par client
    path('edit_fac/<int:facture_id>/',updateFac,name='edit_Fac'), # Mise à jour de la Facture
    path('supp_fac/<int:facture_id>/', deleteFac, name='supp_fac'),  # Suppression de la Facture
    #Honoraire
    path('list_hon/<int:client_id>/',listHon, name='list_Hon'),# Liste Honoraire
    path('nh/new/', create_nh, name='create_nh'), # Creation des Honoraires

    #Description
    path('description_fac/<int:facture_id>',add_description, name='add_description'),#Description Facture
    path('update_description/<int:description_id>',update_Description, name='update_description'),#Modification Description
    path('delete_description/<int:description_id>',deleteDesc, name='delete_description'),#Suppression de la description
    path('nh/<int:nh_id>/description/', add_description_nh, name='add_description_nh'),#Description Honoraire

    ]