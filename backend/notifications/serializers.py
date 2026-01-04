from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'type_notification', 'titre', 'message', 'est_lue',
            'date_creation', 'date_lecture', 'lien_url'
        )
        read_only_fields = ('id', 'date_creation', 'date_lecture')

