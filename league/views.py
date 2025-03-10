from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from geopy.geocoders import Nominatim
import geopandas as gpd
from django.shortcuts import render
from django.http import JsonResponse
import os
import pandas as pd
from .models import Team, Player
from .serializers import TeamSerializer, PlayerSerializer
from .forms import CSVUploadForm
from django.conf import settings

# ViewSets for API
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

# Geocode API View
class GeocodeView(APIView):
    def get(self, request, *args, **kwargs):
        address = request.query_params.get('address', None)
        if not address:
            return Response({"error": "No address provided"}, status=400)
        
        geolocator = Nominatim(user_agent="myApp")
        try:
            location = geolocator.geocode(address)
            if location:
                return Response({
                    "location": location.raw,
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })
            return Response({"error": "Address not found"}, status=404)
        except Exception as e:
            return Response({"error": f"Geocoding failed: {str(e)}"}, status=500)

# Parse KML
def parse_kml(file_path):
    gdf = gpd.read_file(file_path)
    coordinates = []
    polygons = []

    for geom in gdf.geometry:
        if geom.geom_type == 'Point':
            coordinates.append((geom.y, geom.x))  # Latitude, Longitude
        elif geom.geom_type == 'Polygon':
            polygon_coords = list(geom.exterior.coords)
            polygons.append(polygon_coords)
    
    return coordinates, polygons

# Homepage View (using Here Maps)
def homepage(request):
    kml_path = os.path.join(settings.BASE_DIR, 'static', 'District8.kml')
    coordinates, polygons = parse_kml(kml_path)

    if coordinates:
        latitude, longitude = coordinates[0]  # Get the first coordinate from the KML
    else:
        latitude = 39.8850692
        longitude = -86.1849846  # Default coordinates

    return render(request, 'home.html', {
        'latitude': latitude,
        'longitude': longitude,
        'coordinates': coordinates,
        'polygons': polygons,
    })

# CSV Upload View
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        try:
            df = pd.read_csv(csv_file)

            # Check if necessary columns exist in the CSV
            required_columns = ['name', 'age', 'team']
            if not all(col in df.columns for col in required_columns):
                return JsonResponse({"error": f"Missing one or more required columns: {', '.join(required_columns)}"}, status=400)

            for _, row in df.iterrows():
                player = Player(
                    name=row['name'],
                    age=row['age'],
                    team=row['team'],
                )
                player.save()

            return JsonResponse({"message": "CSV file uploaded and data saved!"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return render(request, 'upload_csv.html')