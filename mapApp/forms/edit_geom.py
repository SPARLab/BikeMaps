from django import forms

from crispy_forms.helper import FormHelper


# Used to send polygon info to view
class EditForm(forms.Form):
    helper = FormHelper()
    helper.form_tag = False

    editPk = forms.CharField(
        label = "editPk",
        required = True,
        widget = forms.HiddenInput(attrs={'id': 'editPk'})
    )
    
    editType = forms.CharField(
        label = "editType",
        max_length=10,
        required = True,
        widget = forms.HiddenInput(attrs={'id': 'editType'})
    )
    
    editGeom = forms.CharField(
        label = "Geom",
        required = False,
        widget = forms.HiddenInput(attrs={'id': 'editGeom'})
    )

    objType = forms.CharField(
        label = "objType",
        required = False,
        widget = forms.HiddenInput(attrs={'id': 'objType'})
    )