from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Accordion, AccordionGroup, FormActions, Div
from crispy_forms.layout import Layout, Field, HTML, Button, Submit, Reset, HTML

from mapApp.models import Hazard

class HazardForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        HTML("<br>"),
        Accordion(
            AccordionGroup(
                'Hazard Details',
                Field('geom', type="hidden", id="hazPoint"), # Coords passed after click on map from static/mapApp/js/map.js
                Field('date', id="hazard_date", template='mapApp/util/datepicker.html', autocomplete='off'),
                Field('i_type', id="hazard-type"),#, template='mapApp/util/multiselect_field.html'),
            ),
            AccordionGroup(
                'Description',
                Field('details', placeholder='optional'),
                css_id = 'hazard-description'
            ),
            AccordionGroup(
                'Personal Details',
                HTML("""
                    <a class="text-info" data-toggle="collapse" href=".whyPersonalCollapse" aria-expanded="false" aria-controls="whyPersonalCollapse">
                        <span class="glyphicon glyphicon-question-sign"></span><strong> Why Are We Asking for Personal Details?</strong>
                    </a>
                    <div class="collapse whyPersonalCollapse">
                        <div class="well no-margins">
                            Personal details such as age and gender are routinely collected in health research including studies examining cycling injuries
                            (e.g., Cripton et al. 2015). In addition, details such as rider experience and gender have been shown to be important predictors
                            of cycling safety and risk (Beck et al. 2007). The goal of BikeMaps.org is to gather more comprehensive data to better assess cycling
                            safety and risk. Providing personal details will allow us to more accurately fill in these data gaps.
                        </div>
                    </div>
                """),
                Field('age'),
                Field('birthmonth'),
                Field('sex'),
                Field('regular_cyclist'),
                css_id = 'hazard-personal'
            )
        ),
        Div(
            HTML("""
                <input type='checkbox' class='terms_hazard'>
                <strong> I have read and understand the
                <a href="{% url 'mapApp:termsAndConditions' %}" target=_blank>terms and conditions</a></strong>

                <script>
                  $(".terms_hazard").change(function() {
                    if(this.checked) {
                        $(".submitBtnHazard").removeClass("disabled");
                    }else{
                        $(".submitBtnHazard").addClass("disabled");
                    }
                });

                </script>
            """),
        ),
        Div(
            FormActions(
                Reset('cancel', 'Cancel', onclick="$('#incidentForm').modal('hide');$('.modal-backdrop').hide();"),
                Submit('save', 'Submit', css_class="disabled submitBtnHazard"),
            ),
            css_class='modal-footer'
        ),
    )

    class Meta:
        model = Hazard
        fields = '__all__'
