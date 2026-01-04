from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Modèle pour les notifications utilisateur
    """
    TYPE_CHOICES = [
        ('nouvelle_commande', 'Nouvelle commande'),
        ('commande_confirmee', 'Commande confirmée'),
        ('nouveau_message', 'Nouveau message'),
        ('nouvel_avis', 'Nouvel avis'),
        ('paiement_recu', 'Paiement reçu'),
        ('service_annule', 'Service annulé'),
        ('rappel', 'Rappel'),
    ]
    
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    type_notification = models.CharField(max_length=50, choices=TYPE_CHOICES)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    est_lue = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(null=True, blank=True)
    
    # Lien optionnel vers un objet (transaction, message, etc.)
    lien_url = models.URLField(blank=True)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['utilisateur', 'est_lue']),
            models.Index(fields=['utilisateur', 'date_creation']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.utilisateur.username}"
    
    def marquer_comme_lue(self):
        """Marque la notification comme lue"""
        if not self.est_lue:
            from django.utils import timezone
            self.est_lue = True
            self.date_lecture = timezone.now()
            self.save(update_fields=['est_lue', 'date_lecture'])

