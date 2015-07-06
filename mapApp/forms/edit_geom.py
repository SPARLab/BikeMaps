from django import forms

# Used to send polygon info to view
class EditForm(forms.Form):
    editPk = forms.CharField(
        label = "editPk",
        required = True,
    )

    editType = forms.CharField(
        label = "editType",
        max_length=10,
        required = True,
    )

    editGeom = forms.CharField(
        label = "Geom",
        required = False,
    )

    objType = forms.CharField(
        label = "objType",
        required = False,
    )
