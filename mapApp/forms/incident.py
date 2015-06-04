from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as trans
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
                _('Incident Details'),
                Field('geom', type="hidden", id="point"), # Coords passed after click on map from static/mapApp/js/map.js
                Field('date', id="incident_date", template='mapApp/util/datepicker.html', autocomplete='off'),
                Field('i_type'),
                Field('incident_with'),
                Field('injury'),
                Field('trip_purpose'),
            ),
            AccordionGroup(
                _('Conditions'),
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
                _('Description'),
                Field('details', placeholder=_('optional')),
                css_id='incident-description'
            ),
            AccordionGroup(
                _('Personal Details'),
                HTML("""
                    <a class="text-info" data-toggle="collapse" href=".whyPersonalCollapse" aria-expanded="false" aria-controls="whyPersonalCollapse">
                        <span class="glyphicon glyphicon-question-sign"></span><strong> {0}</strong>
                    </a>
                    <div class="collapse whyPersonalCollapse">
                        <div class="well no-margins">
                            {1}
                        </div>
                    </div>
                """.format(trans("Why Are We Asking for Personal Details?"), trans("""Personal details such as age and gender are routinely collected in health research including studies examining cycling injuries
                (e.g., Cripton et al. 2015). In addition, details such as rider experience and gender have been shown to be important predictors of cycling safety and risk (Beck et al. 2007). The goal of BikeMaps.org is to gather more comprehensive data to better assess cycling safety and risk. Providing personal details will allow us to more accurately fill in these data gaps."""))),

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
                <input type='checkbox' class='terms_hazard'>
                <strong> {0}</strong>

                <script>
                  $(".terms_hazard").change(function() {{
                    if(this.checked) {{
                        $(".submitBtnHazard").removeClass("disabled");
                    }}else{{
                        $(".submitBtnHazard").addClass("disabled");
                    }}
                }});

                </script>
                """.format(trans('I have read and understand the <a href=\'{% url "mapApp:termsAndConditions" %}\' target=_blank> terms and conditions</a>'),)
            ),
        ),
        Div(
            FormActions(
                Reset('cancel', _('Cancel'), onclick="$('#incidentForm').modal('hide');$('.modal-backdrop').hide();"),
                Submit('save', _('Submit'), css_class="disabled submitBtnIncident"),
            ),
            css_class='modal-footer'
        ),
    )

    class Meta:
        model = Incident
        fields = '__all__'
