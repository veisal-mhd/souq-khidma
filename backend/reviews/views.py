from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les avis et évaluations
    """
    queryset = Review.objects.filter(est_approuve=True)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prestataire', 'service', 'note']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def signaler(self, request, pk=None):
        """Permet de signaler un avis inapproprié"""
        review = self.get_object()
        review.est_signale = True
        review.save(update_fields=['est_signale'])
        return Response({'message': 'Avis signalé avec succès'})

