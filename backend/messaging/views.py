from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, MessageSerializer, MessageCreateSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les conversations
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Retourne les conversations où l'utilisateur est participant
        return Conversation.objects.filter(participants=self.request.user)
    
    @action(detail=False, methods=['get'])
    def avec_utilisateur(self, request):
        """Récupère ou crée une conversation avec un utilisateur spécifique"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from accounts.models import User
            autre_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Utilisateur introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Chercher une conversation existante
        conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=autre_user
        ).distinct().first()
        
        if not conversation:
            # Créer une nouvelle conversation
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, autre_user)
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les messages
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
    
    def get_queryset(self):
        # Retourne les messages des conversations de l'utilisateur
        conversations = Conversation.objects.filter(participants=self.request.user)
        return Message.objects.filter(conversation__in=conversations)
    
    @action(detail=True, methods=['post'])
    def marquer_lu(self, request, pk=None):
        """Marque un message comme lu"""
        message = self.get_object()
        message.marquer_comme_lu()
        return Response(MessageSerializer(message).data)
    
    @action(detail=False, methods=['get'])
    def non_lus(self, request):
        """Retourne le nombre de messages non lus"""
        conversations = Conversation.objects.filter(participants=request.user)
        messages_non_lus = Message.objects.filter(
            conversation__in=conversations,
            est_lu=False
        ).exclude(expediteur=request.user).count()
        
        return Response({'nombre_messages_non_lus': messages_non_lus})

