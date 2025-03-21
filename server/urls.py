from django.urls import path, include
from rest_framework.routers import DefaultRouter
from organizations_manager_app.views import OrganizationViewSet, OwnershipStructureViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'ownership-structures', OwnershipStructureViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]