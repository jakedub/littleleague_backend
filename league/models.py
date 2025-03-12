from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)  # Nullable field
    latitude = models.FloatField(null=True, blank=True)  # Add latitude field
    longitude = models.FloatField(null=True, blank=True)
    district = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"