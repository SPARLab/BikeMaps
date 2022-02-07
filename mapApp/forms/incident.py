from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div
from crispy_forms.bootstrap import Accordion, AccordionGroup

from mapApp.models import Incident
import datetime

why_personal_link = format_lazy('<a class="text-info" data-toggle="collapse" aria-expanded="false" aria-controls="why-personal" href=".tab-pane.active .why-personal"><span class="glyphicon glyphicon-question-sign"></span> <strong>{why} </strong></a>', why=_("Why are we asking for personal details?"))

why_personal_well = _("Personal details such as age and gender are routinely collected in health research including studies examining cycling injuries (e.g., Cripton et al. 2015). In addition, details such as rider experience and gender have been shown to be important predictors of cycling safety and risk (Beck et al. 2007). The goal of BikeMaps.org is to gather more comprehensive data to better assess cycling safety and risk. Providing personal details will allow us to more accurately fill in these data gaps.")


class IncidentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template
    helper.disable_csrf = True

    helper.layout = Layout(
        Accordion(
            AccordionGroup(
                _('Collision Details'),
                Field('geom', type='hidden', id='point'),
                Field('personal_involvement', id='incident_personal_involvement'),
                Field('witness_vehicle', id='incident_witness_vehicle'),
                Field('date', id='incident_date', template='mapApp/util/%s_datepicker.html', autocomplete='off'),
                Field('i_type', id='incident_i_type'),
                Field('incident_with', id='incident_incident_with'),
                Field('bicycle_type', id='incident_bicycle_type'),
                Field('ebike', id='incident_ebike'),
                Field('injury', id='incident_injury'),
                Field('impact', id='incident_impact'),
                Field('trip_purpose', id='incident_trip_purpose'),
                Field('details', id='collision_details', placeholder=_('required'))
            ),
            AccordionGroup(
                _('Conditions'),
                Field('road_conditions', id='incident_road_conditions'),
                Field('sightlines', id='incident_sightlines'),
                Field('cars_on_roadside', id='incident_cars_on_roadside'),
                Field('bike_lights', id='incident_bike_lights'),
                Field('terrain', id='incident_terrain'),
                Field('direction', id='incident_direction'),
                Field('turning', id='incident_turning'),
                Field('intersection', id='incident_intersection'),
                Field('aggressive', id='incident_aggressive'),
                css_id='incident-conditions',
            ),
            AccordionGroup(
                _('Personal Details'),
                HTML(why_personal_link),
                Div( Div(HTML(why_personal_well), css_class="well"), css_class='why-personal collapse' ),
                Field('source', id='incident_source'),
                Field('age', id='incident_age'),
                Field('birthmonth', id='incident_birthmonth'),
                Field('sex', id='incident_sex'),
                Field('regular_cyclist', id='incident_regular_cyclist'),
                Field('helmet', id='incident_helmet'),
                css_id='incident-personal-details',
            ),
        )
    )

    def is_valid(self):

        # run default, parent validation first
        # if failed, get results with super(IncidentForm, self).errors
        valid = super(IncidentForm, self).is_valid()

        # check date to ensure incident occurred within the past 2 years
        limit = datetime.timedelta(weeks=-104)
        min_date = datetime.datetime.today() + limit
        # hack fix because app is not time zone aware and we are trying to test dates in different time zones
        max_date = datetime.datetime.today() + datetime.timedelta(days=1)
        if 'date' in self.cleaned_data:
            submitted_date = self.cleaned_data['date']
            if submitted_date > max_date:
                self._errors['date'] = [_('The date can\'t be in the future.')]
                return False
            if submitted_date < min_date:
                self._errors['date'] = [_('Incidents must have occurred within the past two years.')]
                return False
        return valid

    class Meta:
        model = Incident
        exclude = ['p_type']
