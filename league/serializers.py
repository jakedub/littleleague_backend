from rest_framework import serializers
from .models import Team, Player, Evaluation, Division

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['name']

class PlayerSerializer(serializers.ModelSerializer):
    division = DivisionSerializer(read_only=True)
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'street_address', 'city', 'state', 'postal_code', 'latitude', 'longitude', 'division']

class EvaluationSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)  # Include full player details in the response

    class Meta:
        model = Evaluation
        fields = ['id', 'player', 'season_year', 'evaluation_type', 'hitting_power', 
                  'hitting_contact', 'hitting_form', 'fielding_form', 'fielding_glove', 
                  'fielding_hustle', 'throwing_form', 'throwing_accuracy', 'throwing_speed', 
                  'pitching_speed', 'pitching_accuracy']