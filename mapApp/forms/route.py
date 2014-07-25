from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Accordion, AccordionGroup
from crispy_forms.layout import Layout, Field

from mapApp.models.route import Route


class RouteForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        Accordion(
            AccordionGroup(
                'Details',
                Field('trip_purpose'),
                Field('frequency'),
                Field('geom', type="hidden", id="line"), # Coords passed after clicks on map
            ),
        )
    )

    class Meta:
        model = Route