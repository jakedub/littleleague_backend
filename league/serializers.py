from rest_framework import serializers
from .models import Team, Player, Evaluation

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'city']

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'street_address', 'city', 'state', 'postal_code', 'latitude', 'longitude', 'district']

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['id', 'player', 'season_year', 'evaluation_type', 'hitting_power', 'hitting_contact', 'hitting_form', 'fielding_form', 'fielding_glove', 'fielding_hustle', 'throwing_form', 'throwing_accuracy', 'throwing_speed', 'pitching_speed', 'pitching_accuracy']