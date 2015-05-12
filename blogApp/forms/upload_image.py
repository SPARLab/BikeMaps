from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Div
from crispy_forms.layout import Layout, Field, HTML, Button, Submit, Reset

class UploadImageForm(forms.Form):
    helper = FormHelper()
    helper.form_tag = False
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-xs-3'
    helper.field_class = 'col-xs-9'

    title = forms.CharField(
        label = "Alt. Title",
        required = True,
        max_length=50,
    )

    image = forms.FileField(
        label = "Image",
        required = True,
    )

    resize = forms.IntegerField(
        label = "Resize to this width or height",
        initial = 1000,
        required = True,
    )

    helper.layout = Layout(
        Field('title'),
        Field('image'),
        Field('resize'),

        Div(
            FormActions(
                HTML('<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>'),
                Submit('save', 'Upload'),
            ),
            css_class="modal-footer"
        ),

    )
