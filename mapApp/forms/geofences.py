from django import forms
from mapApp.models import AlertArea

class GeofenceForm(forms.ModelForm):
    class Meta:
        model = AlertArea
        fields = ['user', 'geom', 'email']
