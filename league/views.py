from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from geopy.geocoders import Nominatim
from django.shortcuts import render
from .models import Team, Player
from .serializers import TeamSerializer, PlayerSerializer

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
        if address:
            geolocator = Nominatim(user_agent="myApp")
            location = geolocator.geocode(address)
            return Response({"location": location.raw if location else "Not found"})
        return Response({"error": "No address provided"}, status=400)

# Homepage View
def homepage(request):
    return render(request, 'home.html')  # Create a simple home.html template
