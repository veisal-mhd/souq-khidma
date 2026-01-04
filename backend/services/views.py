from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Categorie, Service, Forfait
from .serializers import (
    CategorieSerializer, ServiceSerializer, ServiceCreateSerializer, ForfaitSerializer
)


class CategorieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les catégories (lecture seule)
    """
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les services avec recherche et filtres
    """
    queryset = Service.objects.filter(est_actif=True)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categorie', 'disponibilite', 'ville', 'prestataire']
    search_fields = ['titre', 'description', 'ville', 'quartier']
    ordering_fields = ['date_creation', 'prix', 'nombre_vues', 'nombre_commandes']
    ordering = ['-date_creation']
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ServiceCreateSerializer
        return ServiceSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'mes_services']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtre par prix min/max
        prix_min = self.request.query_params.get('prix_min')
        prix_max = self.request.query_params.get('prix_max')
        
        if prix_min:
            queryset = queryset.filter(prix__gte=prix_min)
        if prix_max:
            queryset = queryset.filter(prix__lte=prix_max)
        
        # Services sponsorisés en premier
        if self.request.query_params.get('sponsorise') == 'true':
            queryset = queryset.filter(est_sponsorise=True)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def incrementer_vues(self, request, pk=None):
        """Incrémente le nombre de vues d'un service"""
        service = self.get_object()
        service.nombre_vues += 1
        service.save(update_fields=['nombre_vues'])
        return Response({'nombre_vues': service.nombre_vues})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mes_services(self, request):
        """Retourne les services du prestataire connecté"""
        services = self.queryset.filter(prestataire=request.user)
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)


class ForfaitViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les forfaits
    """
    queryset = Forfait.objects.filter(est_actif=True)
    serializer_class = ForfaitSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['service']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

