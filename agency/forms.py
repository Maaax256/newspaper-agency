from django import forms
from django.contrib.auth import get_user_model
from agency.models import Newspaper, Topic


class NewspaperForm(forms.ModelForm):
    redactors = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Newspaper
        fields = "__all__"