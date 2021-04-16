from rest_framework import views, status
from rest_framework.response import Response
from .models import Compte
from .serializers import CompteSerializer, CompteDetailSerializer, CompteCreateSerializer

class Comptes(views.APIView):
    serializer_class = CompteCreateSerializer
    def get(self, request, pk=None, format=None):
        if pk:
            comptes = Compte.objects.get(pk=pk)
            serializer = CompteDetailSerializer(comptes)
        else:
            comptes = Compte.objects.all()
            serializer = CompteSerializer(comptes, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = CompteCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    "status": "error",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
