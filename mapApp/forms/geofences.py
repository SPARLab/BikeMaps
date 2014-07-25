from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML

from mapApp.models.alert_area import AlertArea


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