from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation', 'date_modification', 'transaction')
    filter_horizontal = ('participants',)
    readonly_fields = ('date_creation', 'date_modification')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('expediteur', 'conversation', 'timestamp', 'est_lu')
    list_filter = ('est_lu', 'timestamp')
    search_fields = ('contenu', 'expediteur__username')
    readonly_fields = ('timestamp', 'date_lecture')

