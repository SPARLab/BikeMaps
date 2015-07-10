from django import forms

# Used to send polygon info to view
class UpdateHazardForm(forms.Form):
    pk = forms.IntegerField()
    fixed = forms.BooleanField(required=False)
