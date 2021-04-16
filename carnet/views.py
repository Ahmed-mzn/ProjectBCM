from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View

from .forms import *
from .models import *
from django.utils import timezone
from django.utils.decorators import method_decorator



class Accueil(View):
    def get(self, request):
        return render(request, 'pages/accueil.html',{'active_page':"Vue"})

class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['active_page'] = "dashboard"
        return render(request, 'pages/dashboard.html', context)


class CompteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/compte.html', {'comptes': Compte.objects.all(),
                                                     'active_page': "compte"})
    def post(self, request, *args, **kwargs):
        context = {}
        context['active_page'] = "compte"
        num_compte = request.POST['numCompte']
        context['carnets'] = CarnetCheque.objects.filter(compte__numero=num_compte).all()
        context['carnetBV'] = CarnetBV.objects.filter(compte__numero=num_compte).all()
        context['compte'] = Compte.objects.get(pk=num_compte)
        return render(request, 'pages/compteDetails.html', context)


class CompteDetailsView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}
        context['active_page'] = "compte"
        return render(request, 'pages/compteDetails.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        context['active_page'] = "compte"
        genre_carnet = request.POST['type']
        id_carnet = request.POST['id_carnet']
        if genre_carnet == "BV":
            carnet = CarnetBV.objects.get(pk=id_carnet)
            context['carnet'] = carnet
            context['type'] = "BV"
            context['agent_creation'] = User.objects.filter(id=carnet.id_agent_Creation).last()
            context['agent_impression'] = User.objects.filter(pk=carnet.id_agent_Impression).last()
            context['agent_emission'] = User.objects.filter(pk=carnet.id_agent_Emission).last()
            context['cheques'] = ChequeBV.objects.filter(carnet=carnet)
            context['nombre_cheques'] = len(context['cheques'])
            return render(request, 'pages/carnetDetails.html', context)
        else:
            carnet = CarnetCheque.objects.get(pk=id_carnet)
            context['carnet'] = carnet
            context['agent_creation'] = User.objects.filter(id=carnet.id_agent_Creation).last()
            context['agent_impression'] = User.objects.filter(pk=carnet.id_agent_Impression).last()
            context['agent_emission'] = User.objects.filter(pk=carnet.id_agent_Emission).last()
            context['cheques'] = Cheque.objects.filter(carnet=carnet)
            context['nombre_cheques'] = len(context['cheques'])
            return render(request, 'pages/carnetDetails.html', context)


class CreationCompteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['active_page'] = "compte"
        return render(request, 'pages/creationCompte.html', context)
    def post(self, request, *args, **kwargs):
        type_compte = request.POST['type']
        if type_compte == 'Organisation':
            numero_compte = request.POST['numCompte']
            numero_org = str(request.POST['numOrg']).zfill(3)
            libelle_compte = request.POST['libelle']
            created_compte = Compte(numero=numero_compte, numOrganisation=numero_org, libelle=libelle_compte)
            created_compte.save()
        else:
            numero_compte = request.POST['numCompte']
            libelle_compte = request.POST['libelle']
            created_compte = Compte(numero=numero_compte, libelle=libelle_compte)
            created_compte.save()
        return redirect('compte')

class CarnetChequeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['carnets'] = CarnetCheque.objects.all()
        context['active_page'] = "carnetCheque"
        return render(request, 'pages/carnetCheque.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        context['active_page'] = "carnetCheque"
        id_carnet = request.POST['id_carnet']
        carnet = CarnetCheque.objects.get(pk=id_carnet)
        context['carnet'] = carnet
        context['agent_creation'] = User.objects.filter(id=carnet.id_agent_Creation).last()
        context['agent_impression'] = User.objects.filter(pk=carnet.id_agent_Impression).last()
        context['agent_emission'] = User.objects.filter(pk=carnet.id_agent_Emission).last()
        context['cheques'] = Cheque.objects.filter(carnet=carnet)
        context['nombre_cheques'] = len(context['cheques'])
        return render(request, 'pages/carnetDetails.html', context)


class CreationCarnetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['active_page'] = "compte"
        num_compte = request.POST['numCompte']
        context['carnets'] = CarnetCheque.objects.filter(compte__numero=num_compte).all()
        context['carnetBV'] = CarnetBV.objects.filter(compte__numero=num_compte).all()
        context['compte'] = Compte.objects.get(pk=num_compte)
        return render(request, 'pages/compteDetails.html', context)

    def post(self, request, *args, **kwargs):
        numeroCompte = request.POST['numCompte']
        nombreCheque = int(request.POST['nombreCheque'])
        compte = Compte.objects.get(pk=numeroCompte)
        num_cheque = ""

        if compte.numOrganisation:
            if not CarnetCheque.objects.filter(compte__numOrganisation=compte.numOrganisation).exists():
                created_carnet = CarnetCheque(statut="Creer", compte=compte, date_Creation=timezone.now(),
                                              id_agent_Creation=request.user.id)
                created_carnet.save()
                for count in range(1, nombreCheque + 1):
                    num_cheque = f"1{str(compte.numOrganisation).zfill(3)}{str(count).zfill(11)}"
                    created_cheque = Cheque(numero=num_cheque, statut="Creer", carnet=created_carnet)
                    created_cheque.save()
            else:
                last_carnet, last_cheque = CarnetCheque.Last(compte)
                created_carnet = CarnetCheque(statut="Creer", compte=compte, date_Creation=timezone.now(),
                                              id_agent_Creation=request.user.id)
                created_carnet.save()
                for count in range(last_cheque + 1, last_cheque + 1 + nombreCheque):
                    num_cheque = f"1{str(compte.numOrganisation).zfill(3)}{str(count).zfill(11)}"
                    created_cheque = Cheque(numero=num_cheque, statut="Creer", carnet=created_carnet)
                    created_cheque.save()


        else:
            if not CarnetCheque.objects.filter(compte__numero=compte.numero).exists():
                created_carnet = CarnetCheque(statut="Creer", compte=compte, date_Creation=timezone.now(),
                                              id_agent_Creation=request.user.id)
                created_carnet.save()
                for count in range(1, nombreCheque + 1):
                    num_cheque = f"{numeroCompte}{str(count).zfill(8)}"
                    created_cheque = Cheque(numero=num_cheque, statut="Creer", carnet=created_carnet)
                    created_cheque.save()

            else:
                last_carnet, last_cheque = CarnetCheque.Last(compte)
                created_carnet = CarnetCheque(statut="Creer", compte=compte, date_Creation=timezone.now(),
                                              id_agent_Creation=request.user.id)
                created_carnet.save()
                for count in range(last_cheque + 1, last_cheque + nombreCheque + 1):
                    num_cheque = f"{numeroCompte}{str(count).zfill(8)}"
                    created_cheque = Cheque(numero=num_cheque, statut="Creer", carnet=created_carnet)
                    created_cheque.save()
        context = {}
        context['active_page'] = "compte"
        num_compte = request.POST['numCompte']
        context['carnets'] = CarnetCheque.objects.filter(compte__numero=num_compte).all()
        context['carnetBV'] = CarnetBV.objects.filter(compte__numero=num_compte).all()
        context['compte'] = Compte.objects.get(pk=num_compte)
        return render(request, 'pages/compteDetails.html', context)

# @login_required(login_url='loginPage')
# def creationCarnet(request):
#     if request.method == 'POST':
#         numeroCompte = request.POST['numCompte']
#         nombreCheque = int(request.POST['nombreCheque'])
#         compte = Compte.objects.get(pk=numeroCompte)
#         num_cheque = ""
#
#         if compte.numOrganisation:
#             if not CarnetCheque.objects.filter(compte__numOrganisation=compte.numOrganisation).exists():
#                 created_carnet = CarnetCheque(statut="Creer", compte=compte, date_Creation=timezone.now(),
#                                               id_agent_Creation=request.user.id)
#                 created_carnet.save()
#                 for count in range(1, nombreCheque + 1):
#                     num_cheque = f"1{str(compte.numOrganisation).zfill(3)}{str(count).zfill(11)}"
#                     created_cheque = Cheque(numero=num_cheque, statut="Creer", carnet=created_carnet)
#                     created_cheque.save()
#             else:
#                 last_carnet, last_cheque = CarnetCheque.Last(compte)
#                 created_carnet = CarnetCheque(statut="Creer", compte=compte, date_Creation=timezone.now(),
#                                               id_agent_Creation=request.user.id)
#                 created_carnet.save()
#                 for count in range(last_cheque + 1, last_cheque + 1 + nombreCheque):
#                     num_cheque = f"1{str(compte.numOrganisation).zfill(3)}{str(count).zfill(11)}"
#                     created_cheque = Cheque(numero=num_cheque, statut="Creer", carnet=created_carnet)
#                     created_cheque.save()
#
#
#         else:
#             if not CarnetCheque.objects.filter(compte__numero=compte.numero).exists():
#                 created_carnet = CarnetCheque(statut="Creer", compte=compte, date_Creation=timezone.now(),
#                                               id_agent_Creation=request.user.id)
#                 created_carnet.save()
#                 for count in range(1, nombreCheque + 1):
#                     num_cheque = f"{numeroCompte}{str(count).zfill(8)}"
#                     created_cheque = Cheque(numero=num_cheque, statut="Creer", carnet=created_carnet)
#                     created_cheque.save()
#
#             else:
#                 last_carnet, last_cheque = CarnetCheque.Last(compte)
#                 created_carnet = CarnetCheque(statut="Creer", compte=compte, date_Creation=timezone.now(),
#                                               id_agent_Creation=request.user.id)
#                 created_carnet.save()
#                 for count in range(last_cheque + 1, last_cheque + nombreCheque + 1):
#                     num_cheque = f"{numeroCompte}{str(count).zfill(8)}"
#                     created_cheque = Cheque(numero=num_cheque, statut="Creer", carnet=created_carnet)
#                     created_cheque.save()
#         context = {}
#         context['active_page'] = "compte"
#         num_compte = request.POST['numCompte']
#         context['carnets'] = CarnetCheque.objects.filter(compte__numero=num_compte).all()
#         context['carnetBV'] = CarnetBV.objects.filter(compte__numero=num_compte).all()
#         context['compte'] = Compte.objects.get(pk=num_compte)
#         return render(request, 'pages/compteDetails.html', context)
#     else:
#         # context = {}
#         # context['comptes'] = Compte.objects.all()
#         # context['active_page'] = "carnetCheque"
#         # return render(request, 'pages/creationCarnet.html', context)
#         context = {}
#         context['active_page'] = "compte"
#         num_compte = request.POST['numCompte']
#         context['carnets'] = CarnetCheque.objects.filter(compte__numero=num_compte).all()
#         context['carnetBV'] = CarnetBV.objects.filter(compte__numero=num_compte).all()
#         context['compte'] = Compte.objects.get(pk=num_compte)
#         return render(request, 'pages/compteDetails.html', context)

class CarnetDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['active_page'] = "carnetCheque"
        return render(request, 'pages/carnetDetails.html', context)

class CarnetBvView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['carnets'] = CarnetBV.objects.all()
        context['active_page'] = "carnetBV"
        return render(request, 'pages/carnetBV.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        context['active_page'] = "carnetCheque"
        id_carnet = request.POST['id_carnet']
        carnet = CarnetBV.objects.get(pk=id_carnet)
        context['carnet'] = carnet
        context['agent_creation'] = User.objects.filter(id=carnet.id_agent_Creation).last()
        context['agent_impression'] = User.objects.filter(pk=carnet.id_agent_Impression).last()
        context['agent_emission'] = User.objects.filter(pk=carnet.id_agent_Emission).last()
        context['cheques'] = ChequeBV.objects.filter(carnet=carnet)
        context['nombre_cheques'] = len(context['cheques'])
        return render(request, 'pages/carnetBvDetails.html', context)
#
# @login_required(login_url='loginPage')
# def carnetBV(request):
#     if request.method == 'POST':
#         context = {}
#         context['active_page'] = "carnetCheque"
#         id_carnet = request.POST['id_carnet']
#         carnet = CarnetBV.objects.get(pk=id_carnet)
#         context['carnet'] = carnet
#         context['agent_creation'] = User.objects.filter(id=carnet.id_agent_Creation).last()
#         context['agent_impression'] = User.objects.filter(pk=carnet.id_agent_Impression).last()
#         context['agent_emission'] = User.objects.filter(pk=carnet.id_agent_Emission).last()
#         context['cheques'] = ChequeBV.objects.filter(carnet=carnet)
#         context['nombre_cheques'] = len(context['cheques'])
#         return render(request, 'pages/carnetBvDetails.html', context)
#     else:
#         context = {}
#         context['carnets'] = CarnetBV.objects.all()
#         context['active_page'] = "carnetBV"
#         return render(request, 'pages/carnetBV.html', context)

class CreationCarnetBvView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['comptes'] = Compte.objects.filter(numOrganisation__isnull=False)
        context['active_page'] = "carnetBV"
        return render(request, 'pages/creationCarnetBV.html', context)

    def post(self, request, *args, **kwargs):
        numeroCompte = request.POST['numCompte']
        nombreCheque = int(request.POST['nombreCheque'])
        compte = Compte.objects.get(pk=numeroCompte)
        num_cheque = ""

        if compte.numOrganisation:
            if not CarnetBV.objects.filter(compte__numOrganisation=compte.numOrganisation).exists():
                created_carnet = CarnetBV(statut="Creer", compte=compte, date_Creation=timezone.now(),
                                          id_agent_Creation=request.user.id)
                created_carnet.save()
                for count in range(1, nombreCheque + 1):
                    num_cheque = f"9{str(compte.numOrganisation).zfill(3)}{str(count).zfill(11)}"
                    created_cheque = ChequeBV(numero=num_cheque, statut="Creer", carnet=created_carnet)
                    created_cheque.save()
            else:
                last_carnet, last_cheque = CarnetBV.Last(compte)
                created_carnet = CarnetBV(statut="Creer", compte=compte, date_Creation=timezone.now(),
                                          id_agent_Creation=request.user.id)
                created_carnet.save()
                for count in range(last_cheque + 1, last_cheque + 1 + nombreCheque):
                    num_cheque = f"9{str(compte.numOrganisation).zfill(3)}{str(count).zfill(11)}"
                    created_cheque = ChequeBV(numero=num_cheque, statut="Creer", carnet=created_carnet)
                    created_cheque.save()

        context = {}
        context['active_page'] = "compte"
        num_compte = request.POST['numCompte']
        context['carnets'] = CarnetCheque.objects.filter(compte__numero=num_compte).all()
        context['carnetBV'] = CarnetBV.objects.filter(compte__numero=num_compte).all()
        context['compte'] = Compte.objects.get(pk=num_compte)
        return render(request, 'pages/compteDetails.html', context)
#
# @login_required(login_url='loginPage')
# def creationCarnetBV(request):
#     if request.method == 'POST':
#         numeroCompte = request.POST['numCompte']
#         nombreCheque = int(request.POST['nombreCheque'])
#         compte = Compte.objects.get(pk=numeroCompte)
#         num_cheque = ""
#
#         if compte.numOrganisation:
#             if not CarnetBV.objects.filter(compte__numOrganisation=compte.numOrganisation).exists():
#                 created_carnet = CarnetBV(statut="Creer", compte=compte, date_Creation=timezone.now(),
#                                           id_agent_Creation=request.user.id)
#                 created_carnet.save()
#                 for count in range(1, nombreCheque + 1):
#                     num_cheque = f"9{str(compte.numOrganisation).zfill(3)}{str(count).zfill(11)}"
#                     created_cheque = ChequeBV(numero=num_cheque, statut="Creer", carnet=created_carnet)
#                     created_cheque.save()
#             else:
#                 last_carnet, last_cheque = CarnetBV.Last(compte)
#                 created_carnet = CarnetBV(statut="Creer", compte=compte, date_Creation=timezone.now(),
#                                           id_agent_Creation=request.user.id)
#                 created_carnet.save()
#                 for count in range(last_cheque + 1, last_cheque + 1 + nombreCheque):
#                     num_cheque = f"9{str(compte.numOrganisation).zfill(3)}{str(count).zfill(11)}"
#                     created_cheque = ChequeBV(numero=num_cheque, statut="Creer", carnet=created_carnet)
#                     created_cheque.save()
#
#         context = {}
#         context['active_page'] = "compte"
#         num_compte = request.POST['numCompte']
#         context['carnets'] = CarnetCheque.objects.filter(compte__numero=num_compte).all()
#         context['carnetBV'] = CarnetBV.objects.filter(compte__numero=num_compte).all()
#         context['compte'] = Compte.objects.get(pk=num_compte)
#         return render(request, 'pages/compteDetails.html', context)
#     else:
#         context = {}
#         context['comptes'] = Compte.objects.filter(numOrganisation__isnull=False)
#         context['active_page'] = "carnetBV"
#         return render(request, 'pages/creationCarnetBV.html', context)


@login_required(login_url='loginPage')
def deconnecter(request):
    logout(request)
    return redirect('loginPage')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, "nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'pages/login.html')
