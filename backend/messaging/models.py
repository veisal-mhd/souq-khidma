from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """
    Modèle pour les conversations entre utilisateurs
    """
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    # Lien optionnel avec une transaction
    transaction = models.ForeignKey(
        'transactions.Transaction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations'
    )
    
    class Meta:
        db_table = 'conversations'
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        ordering = ['-date_modification']
    
    def __str__(self):
        participants = ", ".join([p.username for p in self.participants.all()])
        return f"Conversation: {participants}"


class Message(models.Model):
    """
    Modèle pour les messages dans les conversations
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    expediteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_envoyes')
    contenu = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    est_lu = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True)
    
    # Fichiers joints
    fichier_joint = models.FileField(upload_to='messages/', null=True, blank=True)
    
    class Meta:
        db_table = 'messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['conversation', 'timestamp']),
            models.Index(fields=['expediteur', 'timestamp']),
        ]
    
    def __str__(self):
        return f"Message de {self.expediteur.username} - {self.timestamp}"
    
    def marquer_comme_lu(self):
        """Marque le message comme lu"""
        if not self.est_lu:
            from django.utils import timezone
            self.est_lu = True
            self.date_lecture = timezone.now()
            self.save(update_fields=['est_lu', 'date_lecture'])

