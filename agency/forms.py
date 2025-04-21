from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from agency.models import Newspaper, Topic, Redactor


def years_of_experience_validation(years: int):
    if years < 0:
        raise forms.ValidationError("The number of years of experience "
                                    "cannot be less than zero.")
    if years > 60:
        raise forms.ValidationError("The number of years of experience "
                                    "cannot be more than 60.")
    return years


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


class RedactorCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )
    years_of_experience = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "years_of_experience"
        )

    def clean_years_of_experience(self):
        years = self.cleaned_data["years_of_experience"]
        years_of_experience_validation(years)
        return years


class RedactorUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "years_of_experience"
        )

    def clean_years_of_experience(self):
        years = self.cleaned_data["years_of_experience"]
        years_of_experience_validation(years)
        return years