from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div
from crispy_forms.bootstrap import Accordion, AccordionGroup

from mapApp.models import NewInfrastructure

class NewInfrastructureForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template
    helper.disable_csrf = True

    helper.layout = Layout(
        Accordion(
            AccordionGroup(
                _('New Infrastructure Details'),
                Field('geom', type='hidden', id='newInfraPoint'),
                Field('dateAdded', id='newInfrastructure_date', template='mapApp/util/%s_datepicker.html', autocomplete='off'),
                Field('infra_type', id=''),
                Field('expires_date', id='newInfrastructure_expiresDate', template='mapApp/util/%s_datepicker_future.html', autocomplete='off'),
                Field('infraDetails', default='Previous reports at this location were reset.'),
            ),
        )
    )

    class Meta:
        model = NewInfrastructure
        exclude = ['p_type','date','details']