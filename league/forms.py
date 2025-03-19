from django import forms
from .models import Evaluation

class EvaluationBulkEditForm(forms.Form):
    season_year = forms.IntegerField(required=True)
    evaluation_type = forms.ChoiceField(choices=Evaluation.EVALUATION_TYPE_CHOICES, required=True)
    hitting_power = forms.IntegerField(min_value=1, max_value=5, required=True)
    hitting_contact = forms.IntegerField(min_value=1, max_value=5, required=True)
    hitting_form = forms.IntegerField(min_value=1, max_value=5, required=True)
    fielding_form = forms.IntegerField(min_value=1, max_value=5, required=True)
    fielding_glove = forms.IntegerField(min_value=1, max_value=5, required=True)
    fielding_hustle = forms.IntegerField(min_value=1, max_value=5, required=True)
    throwing_form = forms.IntegerField(min_value=1, max_value=5, required=True)
    throwing_accuracy = forms.IntegerField(min_value=1, max_value=5, required=True)
    throwing_speed = forms.IntegerField(min_value=1, max_value=5, required=True)
    pitching_speed = forms.IntegerField(min_value=1, max_value=5, required=True)
    pitching_accuracy = forms.IntegerField(min_value=1, max_value=5, required=False)