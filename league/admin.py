from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Team, Player, Evaluation, Division
from .forms import EvaluationBulkEditForm

# Inline model for Evaluations within PlayerAdmin
class EvaluationInline(admin.TabularInline):
    model = Evaluation
    extra = 1  # Show empty row for new entries
    fields = ('season_year', 'evaluation_type', 'hitting_power', 'hitting_contact', 'hitting_form',
              'fielding_form', 'fielding_glove', 'fielding_hustle', 'throwing_form', 'throwing_accuracy',
              'throwing_speed', 'pitching_speed', 'pitching_accuracy')

# Custom Admin for Player to list players and allow bulk edits
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'division', 'edit_evaluations')
    list_filter = ('division',)
    search_fields = ('first_name', 'last_name')
    actions = ['bulk_edit_evaluations']  # Bulk edit action

    def get_queryset(self, request):
        """
        Customize the queryset to filter players by division.
        """
        queryset = super().get_queryset(request)
        division_id = request.GET.get('division')
        if division_id:
            queryset = queryset.filter(division_id=division_id)
        return queryset

    def edit_evaluations(self, obj):
        # Create a custom link to edit evaluations for each player
        return f"<a href='/admin/league/player/{obj.pk}/change/'>Edit Evaluations</a>"
    edit_evaluations.allow_tags = True
    edit_evaluations.short_description = "Edit Evaluations"

    def bulk_edit_evaluations(self, request, queryset):
        """
        Bulk edit evaluations for selected players.
        """
        if 'apply' in request.POST:
            # Process form data for each selected player
            for player in queryset:
                # Collect evaluation data for each player
                season_year = request.POST.get(f"season_year_{player.id}")
                evaluation_type = request.POST.get(f"evaluation_type_{player.id}")
                hitting_power = request.POST.get(f"hitting_power_{player.id}")
                hitting_contact = request.POST.get(f"hitting_contact_{player.id}")
                hitting_form = request.POST.get(f"hitting_form_{player.id}")
                fielding_form = request.POST.get(f"fielding_form_{player.id}")
                fielding_glove = request.POST.get(f"fielding_glove_{player.id}")
                fielding_hustle = request.POST.get(f"fielding_hustle_{player.id}")
                throwing_form = request.POST.get(f"throwing_form_{player.id}")
                throwing_accuracy = request.POST.get(f"throwing_accuracy_{player.id}")
                throwing_speed = request.POST.get(f"throwing_speed_{player.id}")
                pitching_speed = request.POST.get(f"pitching_speed_{player.id}")
                pitching_accuracy = request.POST.get(f"pitching_accuracy_{player.id}")

                # Save or update the evaluation
                evaluation, created = Evaluation.objects.get_or_create(
                    player=player,
                    season_year=season_year,
                    evaluation_type=evaluation_type
                )

                # Update the evaluation fields
                evaluation.hitting_power = hitting_power
                evaluation.hitting_contact = hitting_contact
                evaluation.hitting_form = hitting_form
                evaluation.fielding_form = fielding_form
                evaluation.fielding_glove = fielding_glove
                evaluation.fielding_hustle = fielding_hustle
                evaluation.throwing_form = throwing_form
                evaluation.throwing_accuracy = throwing_accuracy
                evaluation.throwing_speed = throwing_speed
                evaluation.pitching_speed = pitching_speed
                evaluation.pitching_accuracy = pitching_accuracy
                evaluation.save()

            self.message_user(request, "Evaluations updated successfully for selected players!")
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = EvaluationBulkEditForm()

        # Render the bulk edit form
        return render(request, 'admin/bulk_edit_evaluations.html', {'form': form, 'players': queryset})

    bulk_edit_evaluations.short_description = "Bulk edit evaluations for selected players"

# Register models with custom Admin
admin.site.register(Team)
admin.site.register(Player, PlayerAdmin)  # Custom PlayerAdmin with bulk edit
admin.site.register(Evaluation)
admin.site.register(Division)