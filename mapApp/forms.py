from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Accordion, AccordionGroup
from crispy_forms.layout import Layout, Field

from mapApp.models import Incident, Route, AlertArea

class IncidentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        Accordion(
            AccordionGroup(
                'Incident',
                Field('geom', type="hidden", id="geom"), # Coords passed after click on map from static/mapApp/js/map.js
                Field('incident_date', id="incident_date", template='mapApp/util/datepicker.html'),
                Field('incident'),
                Field('incident_with'),
                Field('injury'),
                Field('trip_purpose'),
            ),
            AccordionGroup(
                'Personal Details',
                Field('age'),
                Field('sex'),
                Field('regular_cyclist'),
                Field('helmet'),
                Field('intoxicated'),
            ),
            AccordionGroup(
                'Conditions',
                Field('road_conditions'),
                Field('sightlines'),
                Field('cars_on_roadside'),
                Field('riding_on'),
                Field('bike_lights'),
                Field('terrain'),
            ),
            AccordionGroup(
                'Details',
                Field('incident_detail', placeholder='optional'),
            ),
        )
    )

    class Meta:
        model = Incident


class RouteForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        Accordion(
            AccordionGroup(
                'Details',
                Field('trip_purpose'),
                Field('frequency'),
                Field('line', type="hidden", id="line"), # Coords passed after clicks on map
            ),
        )
    )

    class Meta:
        model = Route


class GeofenceForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        Field('geofence', type="hidden", id="geofence"), # Coords passed after clicks on map
        Field('user', type="hidden"),
        Field('email', readonly=True, id="userEmail"),
        Field('emailWeekly')
    )

    class Meta:
        model = AlertArea


class EmailForm(forms.Form):
    helper = FormHelper()
    helper.form_tag = False

    sender = forms.EmailField(
        label = "Email",
        required = True,
        widget=forms.TextInput(attrs={'placeholder':"Enter your email address"})
    )
    
    subject = forms.CharField(
        label = "Subject",
        max_length=100,
        required = False,
        widget=forms.TextInput(attrs={'placeholder': 'What\'s this about?'})
    )
    
    message = forms.CharField(
        label = "Message",
        required = True,
        widget=forms.Textarea(attrs={'placeholder':"Your message here"})
    )
    
    cc_myself = forms.BooleanField(
        label = "Send myself a copy",
        required=False,
        widget=forms.CheckboxInput()
    )