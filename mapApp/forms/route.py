from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Accordion, AccordionGroup
from crispy_forms.layout import Layout, Field, HTML

from mapApp.models.route import Route


class RouteForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        HTML("""<!-- Modal form -->
                <div class="modal fade" id="routeForm" tabindex="-1" role="dialog" aria-labelledby="routeForm" aria-hidden="false">
                    <div class="modal-dialog">
                        <div class="modal-content">

                            <div class="modal-header">
                                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                <h4 class="modal-title" id="routeForm">Submit your cycling route</h4>
                            </div>
                        
                            <form action="{% url 'mapApp:postRoute' %}" method="post" class="form">
                                {% csrf_token %}
                                <div class="modal-body">"""
        ),


        Accordion(
            AccordionGroup(
                'Details',
                Field('trip_purpose'),
                Field('frequency'),
                Field('geom', type="hidden", id="line"), # Coords passed after clicks on map
            ),
        ),
        

        HTML("""                </div>

                                <div class="modal-footer">
                                    <button type="reset" class="btn btn-default" onclick="$('#routeForm').modal('hide');$('.modal-backdrop').hide();">Cancel</button>
                                    <button type="submit" class="btn btn-primary">Submit</button>
                                </div>
                            
                            </form>
                        </div>
                    </div>
                </div>"""
        )
    )

    class Meta:
        model = Route