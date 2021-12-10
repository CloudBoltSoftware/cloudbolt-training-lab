from cars.models import Manufacturer, Make, Trim
from cars.serializers import ManufacturerSerializer, MakeModelSerializer, TrimSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class ManufacturerViewSet(viewsets.ModelViewSet):
    """
    List all manufacturers, or create a new manufacturer.
    """
    lookup_field = 'id'
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class MakeViewSet(viewsets.ModelViewSet):
    """
    List all makes , or create a new make.
    """
    lookup_field = 'id'
    queryset = Make.objects.all()
    serializer_class = MakeModelSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

class TrimViewSet(viewsets.ModelViewSet):
    """
    List all trims, or create a new trim.
    """
    lookup_field = 'id'
    queryset = Trim.objects.all()
    serializer_class = TrimSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ListView(APIView):
    '''
    List all Manufacturers, Make Models, and Trims
    '''

    def get(self, request, *args, **kwargs):
        manufacturers = ManufacturerSerializer(Manufacturer.objects.all(), many=True).data
        vehicles = MakeModelSerializer(Make.objects.all(), many=True).data
        trims = TrimSerializer(Trim.objects.all(), many=True).data

        results = {'Manufacturers': manufacturers, 'Vehicles': vehicles, 'Trims': trims}
        return Response(results)

