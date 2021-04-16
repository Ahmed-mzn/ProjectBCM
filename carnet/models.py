from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_text
from django.urls import reverse

class Compte(models.Model):
    numero = models.CharField(max_length=7, primary_key=True, verbose_name="Numero du compte")
    libelle = models.CharField(max_length=100)
    numOrganisation = models.CharField(max_length=3, null=True, blank=True, verbose_name="Numero d'organisation")

    def __str__(self):
        return self.libelle

    def get_absolute_url(self):
        return reverse("compte", kwargs={"pk": self.numero})


class CarnetCheque(models.Model):
    statut = models.CharField(max_length=10)
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='carnet_cheques')
    date_Creation = models.DateTimeField(null=True)
    id_agent_Creation = models.IntegerField(null=True)
    date_Impression = models.DateTimeField(null=True)
    id_agent_Impression = models.IntegerField(null=True)
    date_Emission = models.DateTimeField(null=True)
    id_agent_Emission = models.IntegerField(null=True)

    class Meta:
        verbose_name="Carnet de Cheque"

    def __str__(self):
        return f"Carnet {smart_text(self.compte.libelle)}"

    def Last(compte: 'Compte'):
        print(Cheque.objects.filter(
            carnet__compte__numOrganisation=compte.numOrganisation
        ).order_by('numero').query)

        last_cheque = Cheque.objects.filter(
            carnet__compte__numOrganisation=compte.numOrganisation
        ).order_by('numero').last()

        return (last_cheque.carnet, int(last_cheque.numero[4:15]))

        # carnet_exist = CarnetCheque.objects.all()
        # carnet_table = []
        # for carnet in carnet_exist:
        #     if carnet.compte.numOrganisation == compte.numOrganisation:
        #         carnet_table.append(carnet.id)
        #
        # last_carnet = max([x for x in carnet_table])
        # last_carnet = CarnetCheque.objects.get(pk=last_carnet)
        #
        # cheque_exist = Cheque.objects.all()
        # cheque_table = []
        # for cheque in cheque_exist:
        #     if cheque.carnet == last_carnet:
        #         cheque_table.append(cheque.numero)
        # last_cheque = max([x for x in cheque_table])
        # last_cheque = int(last_cheque[4:15])
        #
        # return (last_carnet, last_cheque)


class Cheque(models.Model):
    numero = models.CharField(max_length=15, primary_key=True)
    statut = models.CharField(max_length=10)
    carnet = models.ForeignKey(CarnetCheque, on_delete=models.CASCADE)

    def __str__(self):
        return self.numero


class CarnetBV(models.Model):

    statut = models.CharField(max_length=10)
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='carnet_bvs')
    date_Creation = models.DateTimeField(null=True)
    id_agent_Creation = models.IntegerField(null=True)
    date_Impression = models.DateTimeField(null=True)
    id_agent_Impression = models.IntegerField(null=True)
    date_Emission = models.DateTimeField(null=True)
    id_agent_Emission = models.IntegerField(null=True)

    class Meta:
        verbose_name="Carnet de BV"
        verbose_name_plural="Carnet de BV"

    def __str__(self):
        return f"Carnet {smart_text(self.compte.libelle)}"

    def Last(compte: 'Compte'):

        last_cheque = ChequeBV.objects.filter(
            carnet__compte__numOrganisation=compte.numOrganisation
        ).order_by('numero').last()

        return (last_cheque.carnet, int(last_cheque.numero[4:15]))


class ChequeBV(models.Model):
    numero = models.CharField(max_length=15, primary_key=True)
    statut = models.CharField(max_length=10)
    carnet = models.ForeignKey(CarnetBV, on_delete=models.CASCADE)

    class Meta:
        verbose_name="Cheque de BV"
        verbose_name_plural="Cheque de BV"

    def __str__(self):
        return self.numero