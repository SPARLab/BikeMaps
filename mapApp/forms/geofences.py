from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML

from mapApp.models import AlertArea


class GeofenceForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template

    helper.layout = Layout(
        HTML("""<!-- Modal form -->
                <div class="modal fade" id="geofenceForm" tabindex="-1" role="dialog" aria-labelledby="geofenceForm" aria-hidden="false">
                    <div class="modal-dialog">
                        <div class="modal-content">

                            <div class="modal-header">
                                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                <h4 class="modal-title" id="geofenceForm">Receive alerts for the selected area?</h4>
                            </div>

                            <form action="{% url 'mapApp:postAlertPolygon' %}" method="post" class="form">
                                {% csrf_token %}
                                <div class="modal-body">
        """),



        HTML("""<div class="form-group">
                    <label class="col-xs-6 control-label">Reports will be emailed to you at:</label>
                    <div class="col-xs-6">
                        <p class="form-control-static">{{ request.user.email }}</p>
                    </div>
                </div>"""),
        HTML("""<br><div class="col-xs-12"><em>Address can be changed in user preferences.</em></div>"""),


        Field('user', type="hidden", id="user"), # Coords passed after clicks on map
        Field('geom', type="hidden", id="geofence"), # Coords passed after clicks on map
        Field('email', type="hidden", readonly=True, id="userEmail"),




        HTML("""                </div>

                                <div class="modal-footer">
                                    <button type="reset" class="btn btn-default" onclick="$('#geofenceForm').modal('hide');$('.modal-backdrop').hide();">No thanks</button>
                                    <button type="submit" class="btn btn-primary">Yes please!</button>
                                </div>

                            </form>
                        </div>
                    </div>
                </div>
        """)
    )

    class Meta:
        model = AlertArea
        fields = ['user', 'geom', 'email']
