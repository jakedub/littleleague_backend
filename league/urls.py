from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, PlayerViewSet, GeocodeView, homepage

router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)

urlpatterns = router.urls

# Manually adding GeocodeView to urlpatterns
urlpatterns += [
    path('geocode/', GeocodeView.as_view(), name='geocode'),
    path('', homepage, name='home'),  # Add homepage URL path
]
