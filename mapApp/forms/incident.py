from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div
from crispy_forms.bootstrap import Accordion, AccordionGroup

from mapApp.models import Incident
import datetime

why_personal_link = string_concat('<a class="text-info" data-toggle="collapse" aria-expanded="false" aria-controls="why-personal" href=".tab-pane.active .why-personal"><span class="glyphicon glyphicon-question-sign"></span> <strong>', _(u"Why are we asking for personal details?"), '</strong></a>')

why_personal_well = _(u"Personal details such as age and gender are routinely collected in health research including studies examining cycling injuries (e.g., Cripton et al. 2015). In addition, details such as rider experience and gender have been shown to be important predictors of cycling safety and risk (Beck et al. 2007). The goal of BikeMaps.org is to gather more comprehensive data to better assess cycling safety and risk. Providing personal details will allow us to more accurately fill in these data gaps.")


class IncidentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template
    helper.disable_csrf = True

    helper.layout = Layout(
        Accordion(
            AccordionGroup(
                _('Collision Details'),
                Field('geom', type='hidden', id='point'),
                Field('personal_involvement'),
                Field('witness_vehicle'),
                Field('date', id='incident_date', template='mapApp/util/%s_datepicker.html', autocomplete='off'),
                Field('i_type'),
                Field('incident_with'),
                Field('injury'),
                Field('impact'),
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
                Field('intersection'),
                Field('aggressive'),
                css_id='incident-conditions',
            ),
            AccordionGroup(
                _('Description'),
                Field('details', placeholder=_('mandatory')),
                css_id='incident-description',
            ),
            AccordionGroup(
                _('Personal Details'),
                HTML(why_personal_link),
                Div( Div(HTML(why_personal_well), css_class="well"), css_class='why-personal collapse' ),
                Field('source'),
                Field('age'),
                Field('birthmonth'),
                Field('sex'),
                Field('regular_cyclist'),
                Field('bicycle_type'),
                Field('ebike'),
                Field('helmet'),
                css_id='incident-personal-details',
            ),
        )
    )

    def is_valid(self):

        # run default, parent validation first
        valid = super(IncidentForm, self).is_valid()

        # check date to ensure incident occurred within the past 2 years
        limit = datetime.timedelta(weeks=-104)
        min_date = datetime.datetime.today() + limit
        # hack fix because app is not time zone aware and we are trying to test dates in different time zones
        max_date = datetime.datetime.today() + datetime.timedelta(days=1)
        if 'date' in self.cleaned_data:
            submitted_date = self.cleaned_data['date']
            if submitted_date > max_date:
                self._errors['date'] = [_(u'The date can\'t be in the future.')]
                return False
            if submitted_date < min_date:
                self._errors['date'] = [_(u'Incidents must have occurred within the past two years.')]
                return False
        return valid

    class Meta:
        model = Incident
        exclude = ['p_type']
