from django.urls import path, include
from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from waste.views import WasteCategoryViewSet, PickupRequestViewSet

router = routers.DefaultRouter()

router.register(r'waste-categories', WasteCategoryViewSet, basename='waste-category')
router.register(r'pickups', PickupRequestViewSet, basename='pickup')

urlpatterns = [
    path('', include(router.urls)),
    # djoser auth urls
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # API schema and documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]