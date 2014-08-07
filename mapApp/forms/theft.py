from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Accordion, AccordionGroup, FormActions, Div
from crispy_forms.layout import Layout, Field, HTML, Button, Submit, Reset, HTML

from mapApp.models.theft import Theft

class TheftForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        HTML("<br>"),
        Accordion(
            AccordionGroup(
                'Theft',
                Field('geom', type="hidden", id="theftPoint"), # Coords passed after click on map from static/mapApp/js/map.js
                Field('theft_date', id="theft_date", template='mapApp/util/datepicker.html'),
                Field('theft'),
                Field('how_locked'),
                Field('lock'),
                Field('locked_to'),
            ),
            AccordionGroup(
                'Details',
                Field("police_report"),
                Field("insurance_claim"),
                Field('theft_detail', placeholder='optional'),
                css_id = 'theft-description'
            ),
            AccordionGroup(
                'Personal Details',
                Field('regular_cyclist'),
                css_id = 'theft-personal'
            )
        ),
        Div(
            Div(
                HTML("""
                    <input type='checkbox' class='over13theft'><strong> I am over the age of 13</strong>
                    
                    <script>
                      $(".over13theft").change(function() {
                        if(this.checked) {
                            $(".submitBtnTheft").removeClass("disabled");
                        }else{
                            $(".submitBtnTheft").addClass("disabled");
                        }
                    });
                    </script>
                """),
                css_class='pull-left'
            ),
            FormActions(
                Reset('cancel', 'Cancel', onclick="$('#incidentForm').modal('hide');$('.modal-backdrop').hide();"),
                Submit('save', 'Submit', css_class="disabled submitBtnTheft"),
            ),
            css_class='modal-footer'
        ),
    )

    class Meta:
        model = Theft