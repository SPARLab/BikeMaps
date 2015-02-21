from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Accordion, AccordionGroup, FormActions, Div
from crispy_forms.layout import Layout, Field, HTML, Submit, Reset

from mapApp.models import Incident


class IncidentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        HTML("<br>"),
        Accordion(
            AccordionGroup(
                'Incident Details',
                Field('geom', type="hidden", id="point"), # Coords passed after click on map from static/mapApp/js/map.js
                Field('date', id="incident_date", template='mapApp/util/datepicker.html', autocomplete='off'),
                Field('incident_type'),
                Field('incident_with'),
                Field('injury'),
                Field('trip_purpose'),
            ),
            AccordionGroup(
                'Conditions',
                Field('road_conditions'),
                Field('sightlines'),
                Field('cars_on_roadside'),
                Field('riding_on'),
                Field('bike_lights'),
                Field('terrain'),
                Field('direction'),
                Field('turning'),
            ),
            AccordionGroup(
                'Description',
                Field('details', placeholder='optional'),
                css_id='incident-description'
            ),
            AccordionGroup(
                'Personal Details',
                Field('age'),
                Field('birthmonth'),
                Field('sex'),
                Field('regular_cyclist'),
                Field('helmet'),
                Field('intoxicated'),
                css_id = "incident-personal"
            )
        ),
        Div(
            HTML("""
                <input type='checkbox' class='terms_incident'>
                    <strong> I have read and understand the
                    <a href="{% url 'mapApp:termsAndConditions' %}" target=_blank>terms and conditions</a></strong>

                <script>
                  $(".terms_incident").change(function() {
                    if(this.checked) {
                        $(".submitBtnIncident").removeClass("disabled");
                    }else{
                        $(".submitBtnIncident").addClass("disabled");
                    }
                });
                </script>
            """),
        ),
        Div(
            FormActions(
                Reset('cancel', 'Cancel', onclick="$('#incidentForm').modal('hide');$('.modal-backdrop').hide();"),
                Submit('save', 'Submit', css_class="disabled submitBtnIncident"),
            ),
            css_class='modal-footer'
        ),
    )

    class Meta:
        model = Incident
        fields = '__all__'
