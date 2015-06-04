from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as trans
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Div, AppendedText
from crispy_forms.layout import Layout, Field, HTML, Button, Submit, Reset

class UploadImageForm(forms.Form):
    helper = FormHelper()
    helper.form_tag = False
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-xs-3'
    helper.field_class = 'col-xs-9'

    title = forms.CharField(
        label = _("Alt. Title"),
        required = True,
        max_length=50,
    )

    image = forms.FileField(
        label = "Image",
        required = True,
    )

    resize = forms.IntegerField(
        label = _("Resize to this width or height"),
        initial = 1000,
        required = True,
    )

    helper.layout = Layout(
        Field('title'),
        Field('image'),
        # Translators: This is the shortform for pixels
        AppendedText('resize', _('px')),

        Div(
            FormActions(
                HTML('<button type="button" class="btn btn-default" data-dismiss="modal">{}</button>'.format(trans('Close'))),
                Submit('save', _('Upload')),
            ),
            css_class="modal-footer"
        ),

    )
