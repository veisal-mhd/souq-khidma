from rest_framework import serializers
from .models import Conversation, Message
from accounts.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    expediteur = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = (
            'id', 'conversation', 'expediteur', 'contenu', 'timestamp',
            'est_lu', 'date_lecture', 'fichier_joint'
        )
        read_only_fields = ('id', 'timestamp', 'date_lecture')


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    dernier_message = serializers.SerializerMethodField()
    nombre_messages_non_lus = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = (
            'id', 'participants', 'date_creation', 'date_modification',
            'transaction', 'dernier_message', 'nombre_messages_non_lus'
        )
        read_only_fields = ('id', 'date_creation', 'date_modification')
    
    def get_dernier_message(self, obj):
        dernier = obj.messages.last()
        if dernier:
            return MessageSerializer(dernier).data
        return None
    
    def get_nombre_messages_non_lus(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(est_lu=False).exclude(expediteur=request.user).count()
        return 0


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('conversation', 'contenu', 'fichier_joint')
    
    def create(self, validated_data):
        validated_data['expediteur'] = self.context['request'].user
        return super().create(validated_data)

