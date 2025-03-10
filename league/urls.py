from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GeocodeView, UploadCSVView, KMLCoordinatesView  # Correct view imports

# Initialize the default router for API views (optional)
router = DefaultRouter()
urlpatterns = router.urls

# Manually adding GeocodeView and other views to urlpatterns
urlpatterns += [
    path('geocode/', GeocodeView.as_view(), name='geocode'),
    path('upload-csv/', UploadCSVView.as_view(), name='upload_csv'),  # Correctly referenced view
    path('kml-coordinates/', KMLCoordinatesView.as_view(), name='kml_coordinates'),  # Example for KML coordinates
]