from django import forms
from models_app.models import Category


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = []