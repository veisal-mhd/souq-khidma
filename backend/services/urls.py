from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategorieViewSet, ServiceViewSet, ForfaitViewSet

router = DefaultRouter()
router.register(r'categories', CategorieViewSet, basename='categorie')
router.register(r'', ServiceViewSet, basename='service')
router.register(r'forfaits', ForfaitViewSet, basename='forfait')

urlpatterns = [
    path('', include(router.urls)),
]

