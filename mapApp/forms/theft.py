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
                'Theft Details',
                Field('geom', type="hidden", id="theftPoint"), # Coords passed after click on map from static/mapApp/js/map.js
                Field('theft_date', id="theft_date", template='mapApp/util/datepicker.html', autocomplete='off'),
                Field('theft'),
                Field('how_locked'),
                Field('lock'),
                Field('locked_to'),
                Field('lighting'),
                Field('traffic'),
                Field("police_report"),
                Field("insurance_claim"),
            ),
            AccordionGroup(
                'Description',
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
            HTML("""
                <input type='checkbox' class='terms_theft'>
                    <strong> I have read and understand the 
                    <a href="{% url 'mapApp:termsAndConditions' %}" target=_blank>terms and conditions</a></strong>
                
                <script>
                $(".terms_theft").change(function() {
                    if(this.checked) {
                        $(".submitBtnTheft").removeClass("disabled");
                    }else{
                        $(".submitBtnTheft").addClass("disabled");
                    }
                });

                // Dynamically change lock to "NA" if bike not locked
                $("#div_id_lock select option[value='NA']").hide();
                $("#div_id_how_locked select").change( function(){
                    if($(this).val() == 'Not locked'){
                        $("#div_id_lock select").val('NA');
                        $("#div_id_lock select").attr('disabled', true);
                        $("#div_id_lock select option[value='NA']").show();
                    }
                    else{
                        if($("#div_id_lock select").val() == 'NA'){
                            $("#div_id_lock select").val('');
                        }
                        $("#div_id_lock select").attr('disabled', false);
                        $("#div_id_lock select option[value='NA']").hide();
                    }    
                });


                </script>
            """),
        ),
        Div(
            FormActions(
                Reset('cancel', 'Cancel', onclick="$('#incidentForm').modal('hide');$('.modal-backdrop').hide();"),
                Submit('save', 'Submit', css_class="disabled submitBtnTheft"),
            ),
            css_class='modal-footer'
        ),
    )

    class Meta:
        model = Theft
        fields = ['geom', 'theft_date', 'theft', 'how_locked', 
            'lock', 'locked_to', 'lighting', 'traffic', 'police_report', 
            'insurance_claim', 'theft_detail', 'regular_cyclist'
        ]