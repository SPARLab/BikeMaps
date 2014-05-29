from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Accordion, AccordionGroup
from crispy_forms.layout import Layout, Field

from mapApp.models import Incident

class IncidentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        Accordion(
            AccordionGroup(
                'Incident',
                Field('incident_date', readonly='readonly', id="incident_date", template='mapApp/util/datepicker.html'),
                Field('incident'),
                Field('incident_detail', placeholder='optional'),
                Field('point', type="hidden", id="point") # Need to pass point coords separately and convert to proper format in views
            ),
            AccordionGroup(
                'Trip',
                Field('trip_purpose'),
                Field('road_conditions'),
                Field('sightlines'),
                Field('cars_on_roadside'),
                Field('bike_infrastructure'),
                Field('bike_lights'),
                Field('terrain'),
                Field('helmet')
            ),
            AccordionGroup(
                'Person',
                Field('injury'),
                Field('injury_detail', placeholder='optional'),
                Field('age'),
                Field('sex'),
                Field('regular_cyclist')
            )
        )
    )

    class Meta:
        model = Incident