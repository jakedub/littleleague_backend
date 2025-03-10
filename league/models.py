from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Player(models.Model):
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
