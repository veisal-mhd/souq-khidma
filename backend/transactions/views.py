from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Transaction, AbonnementPremium
from .serializers import (
    TransactionSerializer, TransactionCreateSerializer, AbonnementPremiumSerializer
)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les transactions
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['statut', 'mode_paiement']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TransactionCreateSerializer
        return TransactionSerializer
    
    def get_queryset(self):
        user = self.request.user
        # Les clients voient leurs commandes, les prestataires voient leurs ventes
        if user.is_prestataire:
            return Transaction.objects.filter(prestataire=user)
        return Transaction.objects.filter(client=user)
    
    @action(detail=True, methods=['post'])
    def confirmer_paiement(self, request, pk=None):
        """Confirme le paiement d'une transaction (mise en escrow)"""
        transaction = self.get_object()
        
        if transaction.statut != 'paye':
            return Response(
                {'error': 'La transaction doit être payée avant confirmation'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.statut = 'en_escrow'
        from django.utils import timezone
        transaction.date_paiement = timezone.now()
        transaction.save()
        
        return Response(TransactionSerializer(transaction).data)
    
    @action(detail=True, methods=['post'])
    def confirmer_service(self, request, pk=None):
        """Confirme la réalisation du service (libération de l'escrow)"""
        transaction = self.get_object()
        
        if transaction.statut != 'en_escrow':
            return Response(
                {'error': 'La transaction doit être en escrow'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Seul le client peut confirmer
        if transaction.client != request.user:
            return Response(
                {'error': 'Seul le client peut confirmer le service'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        transaction.statut = 'confirme'
        from django.utils import timezone
        transaction.date_confirmation = timezone.now()
        transaction.save()
        
        return Response(TransactionSerializer(transaction).data)
    
    @action(detail=False, methods=['get'])
    def mes_commandes(self, request):
        """Retourne les commandes du client connecté"""
        transactions = Transaction.objects.filter(client=request.user)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mes_ventes(self, request):
        """Retourne les ventes du prestataire connecté"""
        if not request.user.is_prestataire:
            return Response(
                {'error': 'Accès réservé aux prestataires'},
                status=status.HTTP_403_FORBIDDEN
            )
        transactions = Transaction.objects.filter(prestataire=request.user)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)


class AbonnementPremiumViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les abonnements premium (lecture seule pour les utilisateurs)
    """
    serializer_class = AbonnementPremiumSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return AbonnementPremium.objects.filter(prestataire=self.request.user)

