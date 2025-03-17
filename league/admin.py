from django.contrib import admin
from .models import Team, Player, Evaluation, Division

# Register the Team model
admin.site.register(Team)

# Register the Player model
admin.site.register(Player)

# Register the Evaluation model
admin.site.register(Evaluation)

admin.site.register(Division)