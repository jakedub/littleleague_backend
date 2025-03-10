from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, PlayerViewSet, GeocodeView, upload_csv  # Correct view imports

router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)

urlpatterns = router.urls

# Manually adding GeocodeView and other views to urlpatterns
urlpatterns += [
    path('geocode/', GeocodeView.as_view(), name='geocode'),
    path('upload-csv/', upload_csv, name='upload_csv'),  # Correctly referenced view
]