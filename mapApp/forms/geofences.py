from django.utils.translation import ugettext as trans
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
                                <h4 class="modal-title" id="geofenceForm">{0}</h4>
                            </div>

                            <form action="{{% url 'mapApp:postAlertPolygon' %}}" method="post" class="form">
                                {{% csrf_token %}}
                                <div class="modal-body">
            """.format(trans("Receive alerts for the selected area?"))
        ),



        HTML("""<div class="form-group">
                    <label class="col-xs-6 control-label">{0}"</label>
                    <div class="col-xs-6">
                        <p class="form-control-static">{{ request.user.email }}</p>
                    </div>
                </div>""".format(trans("Reports will be emailed to you at:"))),
        HTML("""<br><div class="col-xs-12"><em>{0}"</em></div>""".format(trans("Address can be changed in user preferences."))),


        Field('user', type="hidden", id="user"), # Coords passed after clicks on map
        Field('geom', type="hidden", id="geofence"), # Coords passed after clicks on map
        Field('email', type="hidden", readonly=True, id="userEmail"),




        HTML("""                </div>

                                <div class="modal-footer">
                                    <button type="reset" class="btn btn-default" onclick="$('#geofenceForm').modal('hide');$('.modal-backdrop').hide();">{0}</button>
                                    <button type="submit" class="btn btn-primary">{1}</button>
                                </div>

                            </form>
                        </div>
                    </div>
                </div>
        """.format(trans("No thanks"), trans("Yes please!")))
    )

    class Meta:
        model = AlertArea
        fields = ['user', 'geom', 'email']
