from rest_framework import serializers

from carnet.models import Compte, CarnetCheque


class CarnetChequeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarnetCheque
        fields = ['statut', 'date_Creation', 'id_agent_Creation', 'date_Impression', 'id_agent_Impression',
                  'date_Emission', 'id_agent_Emission']


class CompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = ['numero', 'libelle', 'numOrganisation', ]


class CompteDetailSerializer(serializers.ModelSerializer):
    carnet_cheques = CarnetChequeSerializer(many=True, read_only=True)

    class Meta:
        model = Compte
        fields = ['numero', 'libelle', 'numOrganisation', 'carnet_cheques']


class CompteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = ['numero', 'libelle', 'numOrganisation']

    def validate_numero(self, value):
        if not (len(value) == 7 and str(value).isdigit()):
            raise serializers.ValidationError("Num INVALID !!")
        return value

    def validate_numOrganisation(self, value):
        if not value:
            return
        if not (len(str(value)) <= 3 and str(value).isdigit()):
            raise serializers.ValidationError("Num org INVALID !!")
        return str(int(value))
