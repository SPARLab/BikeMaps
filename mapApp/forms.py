from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Accordion, AccordionGroup, FormActions, Div
from crispy_forms.layout import Layout, Field, HTML, Button, Submit, Reset

from mapApp.models.incident import Incident
from mapApp.models.route import Route
from mapApp.models.alert_area import AlertArea
from mapApp.models.hazard import Hazard


class IncidentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        Accordion(
            AccordionGroup(
                'Incident',
                Field('geom', type="hidden", id="point"), # Coords passed after click on map from static/mapApp/js/map.js
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
                css_id = "incident-personal"
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
                'Description',
                Field('incident_detail', placeholder='optional'),
                css_id='incident-description'
            )
        ),
        Div(
            Div(
                Field('over13'),
                css_class='pull-left'
            ),
            FormActions(
                Reset('cancel', 'Cancel', onclick="$('#incidentForm').modal('hide');$('.modal-backdrop').hide();"),
                Submit('save', 'Submit'),
            ),
            css_class='modal-footer'
        ),
    )

    class Meta:
        model = Incident


class HazardForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        Accordion(
            AccordionGroup(
                'Hazard',
                Field('geom', type="hidden", id="hazPoint"), # Coords passed after click on map from static/mapApp/js/map.js
                Field('hazard_date', id="hazard_date", template='mapApp/util/datepicker.html'),
                Field('hazard'),
                Field('hazard_object'),
            ),
            AccordionGroup(
                'Personal Details',
                Field('age'),
                Field('sex'),
                Field('regular_cyclist'),
                css_id = 'hazard-personal'
            ),
            AccordionGroup(
                'Description',
                Field('hazard_detail', placeholder='optional'),
                css_id = 'hazard-description'
            )
        ),
        Div(
            Div(
                Field('over13'),
                css_class='pull-left'
            ),
            FormActions(
                Reset('cancel', 'Cancel', onclick="$('#incidentForm').modal('hide');$('.modal-backdrop').hide();"),
                Submit('save', 'Submit'),
            ),
            css_class='modal-footer'
        ),
    )

    class Meta:
        model = Hazard


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


class GeofenceForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        Field('geom', type="hidden", id="geofence"), # Coords passed after clicks on map
        # Field('user', readonly=True, id="userName"),
        Field('email', readonly=True, id="userEmail"),
        Field('emailWeekly'),
        # Field('alertPoints'),
        # Field('emailAlertPoints'),
        HTML("""<br><em>Alerts will also continue to appear in the notifications tab of this website</em>""")
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