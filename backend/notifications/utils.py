"""
Utilitaires pour créer des notifications
"""
from .models import Notification


def creer_notification(utilisateur, type_notification, titre, message, lien_url=''):
    """
    Crée une notification pour un utilisateur
    """
    notification = Notification.objects.create(
        utilisateur=utilisateur,
        type_notification=type_notification,
        titre=titre,
        message=message,
        lien_url=lien_url
    )
    return notification

