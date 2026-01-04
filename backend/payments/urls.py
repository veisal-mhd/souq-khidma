from django.urls import path
from .views import initier_paiement, verifier_paiement

urlpatterns = [
    path('initier/', initier_paiement, name='initier_paiement'),
    path('verifier/', verifier_paiement, name='verifier_paiement'),
]

