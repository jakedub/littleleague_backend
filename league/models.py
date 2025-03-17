from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Team(models.Model):
    TYPE_CHOICES = [
        ('baseball', 'Baseball'),
        ('softball', 'Softball')
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='baseball')

    def __str__(self):
        return self.name
    
class Division(models.Model):
    TYPE_CHOICES = [
        ('majors', 'Majors'),
        ('aaa_minor', 'AAA Minor'),
        ('aa_minor', 'AA Minor'),
        ('peewee', 'PeeWee')
    ]
    name = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name
    
class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)  # Nullable field
    latitude = models.FloatField(null=True, blank=True)  # Add latitude field
    longitude = models.FloatField(null=True, blank=True)
    district = models.BooleanField(default=False)
    jersey_size = models.CharField(max_length=10, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True) 
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Evaluation(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="evaluations")
    season_year = models.IntegerField()
    evaluation_type = models.CharField(max_length=10, choices=[("beginning", "Beginning of Year"), ("end", "End of Year")])
    hitting_power = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    hitting_contact = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    hitting_form = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    fielding_form = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    fielding_glove = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    fielding_hustle = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    throwing_form = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    throwing_accuracy = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    throwing_speed = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    pitching_speed = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    pitching_accuracy = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)  # Updated to match the others
    created_at = models.DateTimeField(auto_now_add=True)
