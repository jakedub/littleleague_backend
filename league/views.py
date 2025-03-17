import json
import os
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from geopy.geocoders import Nominatim
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from .models import Player, Team, Evaluation
from .serializers import TeamSerializer, PlayerSerializer, EvaluationSerializer
from django.core.exceptions import ValidationError
import geopandas as gpd
from rest_framework import viewsets
from shapely.geometry import Point, Polygon

# ViewSets for API (if needed in the future)
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


def check_player_in_district(player, polygons):
    # Get player's coordinates (assumed already available)
    player_point = Point(player.longitude, player.latitude)  # Replace with actual coordinates
    for polygon_coords in polygons:
        polygon = Polygon(polygon_coords)
        if polygon.contains(player_point):
            player.district = True  # Player is within district
            player.save()
            return
    player.district = False  # Player is outside district
    player.save()
    
# Geocode API View
class GeocodeView(APIView):  # type: ignore
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

# Parse KML function
def parse_kml(file_path):
    try:
        # Use geopandas to read the KML file and specify the layer
        gdf = gpd.read_file(file_path)

        # Initialize lists for coordinates and polygons
        coordinates = []
        polygons = []

        # Extract coordinates from the geometry column (assuming they are Points or Polygons)
        for geom in gdf.geometry:
            if geom.geom_type == 'Point':
                coordinates.append({'lat': geom.y, 'lng': geom.x})  # Latitude, Longitude
            elif geom.geom_type == 'Polygon':
                # For polygons, store coordinates as a list of points
                polygon_coords = list(geom.exterior.coords)
                polygons.append(polygon_coords)

        return coordinates, polygons
    except Exception as e:
        print(f"Error parsing KML file: {str(e)}")
        return [], []

# API view for fetching parsed KML coordinates
class KMLCoordinatesView(APIView):
    def get(self, request, *args, **kwargs):
        # Path to your KML file
        kml_path = os.path.join(settings.BASE_DIR, 'static', 'District8.kml')
        
        # Parse KML and get coordinates and polygons
        coordinates, polygons = parse_kml(kml_path)

        # Return the coordinates and polygons as JSON
        return Response({'coordinates': coordinates, 'polygons': polygons})

# Upload CSV view to handle the CSV file upload
class UploadCSVView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Get the uploaded file
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the file is a CSV
        if not file.name.endswith('.csv'):
            return Response({"error": "File must be a CSV"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use pandas to read the CSV file
            df = pd.read_csv(file)

            # Process the CSV data here if needed, or just return the data
            # Example: parsing CSV to check column names
            required_columns = ['Account First Name', 'Account Last Name', 'Street Address', 'City', 'State', 'Postal Code']
            for column in required_columns:
                if column not in df.columns:
                    raise ValidationError(f"Missing required column: {column}")

            # Return the CSV content as JSON (you can modify this as needed)
            return Response(df.to_dict(orient='records'), status=status.HTTP_200_OK)
        
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Failed to process file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Homepage view (optional for rendering HTML page)
def home(request):
    kml_path = os.path.join(settings.BASE_DIR, 'static', 'District8.kml')
    coordinates, polygons = parse_kml(kml_path)

    # Convert coordinates and polygons to JSON
    coordinates_json = json.dumps(coordinates)
    polygons_json = json.dumps(polygons)

    return render(request, 'home.html', {
        'coordinates_json': coordinates_json,
        'polygons_json': polygons_json,
    })

class PlayerListView(APIView):
    def get(self, request, *args, **kwargs):
        players = Player.objects.all()  # You can apply filters if needed
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)
    
def player_addresses(request):
    players = Player.objects.all()  # Fetch all players
    return render(request, 'player_addresses.html', {'players': players})


class EvaluationListView(APIView):
    def get(self, request, *args, **kwargs):
        evaluations = Evaluation.objects.all()
        serializer = EvaluationSerializer(evaluations, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            evaluation = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)