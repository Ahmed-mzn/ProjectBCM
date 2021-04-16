from django.urls import path

from . import views
from . import views_api

urlpatterns = [
    path('', views.Accueil.as_view(), name='accueil'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('compte/', views.CompteView.as_view(), name='compte'),
    path('carnetCheque/', views.CarnetChequeView.as_view(), name='carnetCheque'),
    path('carnetBV/', views.CarnetBvView.as_view(), name='carnetBV'),
    path('deconnecter/', views.deconnecter, name='deconnecter'),
    path('accounts/login/', views.loginPage, name='loginPage'),
    path('deconnecter/', views.deconnecter, name='deconnecter'),
    path('creationCompte/', views.CreationCompteView.as_view(), name='creationCompte'),
    path('creationCarnet/', views.CreationCarnetView.as_view(), name='creationCarnet'),
    path('carnetDetails/', views.CarnetDetailsView.as_view(), name='carnetDetails'),
    path('creationCarnetBV/', views.CreationCarnetBvView.as_view(), name='creationCarnetBV'),
    path('compteDetails/', views.CompteDetailsView.as_view(), name='compteDetails'),

    path('api/v1/comptes/', views_api.Comptes.as_view(), name='api_comptes'),
    path('api/v1/comptes/<int:pk>/', views_api.Comptes.as_view(), name='api_comptes'),
]
