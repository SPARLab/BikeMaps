from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Accordion, AccordionGroup, FormActions, Div
from crispy_forms.layout import Layout, Field, HTML, Button, Submit, Reset, HTML

from mapApp.models.hazard import Hazard

class HazardForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        HTML("<br>"),
        Accordion(
            AccordionGroup(
                'Hazard',
                Field('geom', type="hidden", id="hazPoint"), # Coords passed after click on map from static/mapApp/js/map.js
                Field('hazard_date', id="hazard_date", template='mapApp/util/datepicker.html', autocomplete='off'),
                Field('hazard', id="hazard-type"),#, template='mapApp/util/multiselect_field.html'),
            ),
            AccordionGroup(
                'Description',
                Field('hazard_detail', placeholder='optional'),
                css_id = 'hazard-description'
            ),
            AccordionGroup(
                'Personal Details',
                Field('age'),
                Field('sex'),
                Field('regular_cyclist'),
                css_id = 'hazard-personal'
            )
        ),
        Div(
            Div(
                HTML("""
                    <input type='checkbox' class='over13hazard'><strong> I am over the age of 13</strong>
                    
                    <script>
                      $(".over13hazard").change(function() {
                        if(this.checked) {
                            $(".submitBtnHazard").removeClass("disabled");
                        }else{
                            $(".submitBtnHazard").addClass("disabled");
                        }
                    });

                    </script>
                """),
                css_class='pull-left'
            ),
            FormActions(
                Reset('cancel', 'Cancel', onclick="$('#incidentForm').modal('hide');$('.modal-backdrop').hide();"),
                Submit('save', 'Submit', css_class="disabled submitBtnHazard"),
            ),
            css_class='modal-footer'
        ),
    )

    class Meta:
        model = Hazard
