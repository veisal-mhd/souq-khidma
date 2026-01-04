from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, AbonnementPremiumViewSet

router = DefaultRouter()
router.register(r'', TransactionViewSet, basename='transaction')
router.register(r'abonnements', AbonnementPremiumViewSet, basename='abonnement')

urlpatterns = [
    path('', include(router.urls)),
]

