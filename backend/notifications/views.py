from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les notifications (lecture seule pour les utilisateurs)
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(utilisateur=self.request.user)
    
    @action(detail=True, methods=['post'])
    def marquer_lue(self, request, pk=None):
        """Marque une notification comme lue"""
        notification = self.get_object()
        notification.marquer_comme_lue()
        return Response(NotificationSerializer(notification).data)
    
    @action(detail=False, methods=['post'])
    def marquer_toutes_lues(self, request):
        """Marque toutes les notifications comme lues"""
        Notification.objects.filter(
            utilisateur=request.user,
            est_lue=False
        ).update(est_lue=True)
        return Response({'message': 'Toutes les notifications ont été marquées comme lues'})
    
    @action(detail=False, methods=['get'])
    def non_lues(self, request):
        """Retourne le nombre de notifications non lues"""
        count = Notification.objects.filter(
            utilisateur=request.user,
            est_lue=False
        ).count()
        return Response({'nombre_notifications_non_lues': count})

