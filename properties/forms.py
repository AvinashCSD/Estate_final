from django import forms
from .models import State

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter state name'}),
        }
from django import forms
from .models import Plot, State, District, Taluk, RevenueVillage

class PlotForm(forms.ModelForm):
    class Meta:
        model = Plot
        fields = ['state', 'district', 'taluk', 'revenue_village', 'owner', 'survey_no', 'subdivision', 'plot_number', 'dimensions', 'facing', 'price_range','land_image']

    # Optional: Override clean methods if needed for custom validation
from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data
# properties/forms.py
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
