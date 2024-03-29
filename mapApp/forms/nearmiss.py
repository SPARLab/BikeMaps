import datetime

from crispy_forms.bootstrap import Accordion, AccordionGroup, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout
from django import forms
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _
from mapApp.models import Incident, Gender

why_personal_link = format_lazy('<a class="text-info" data-toggle="collapse" aria-expanded="false" aria-controls="why-personal" href=".tab-pane.active .why-personal"><span class="glyphicon glyphicon-question-sign"></span> <strong>{why}</strong></a>', why=_("Why are we asking for personal details?"))

why_personal_well = _("Personal details such as age and gender are routinely collected in health research including studies examining cycling injuries (e.g., Cripton et al. 2015). In addition, details such as rider experience and gender have been shown to be important predictors of cycling safety and risk (Beck et al. 2007). The goal of BikeMaps.org is to gather more comprehensive data to better assess cycling safety and risk. Providing personal details will allow us to more accurately fill in these data gaps.")

class NearmissForm(forms.ModelForm):
    [...]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False # removes auto-inclusion of form tag in template
        self.helper.disable_csrf = True
        self.fields['gender'].label_from_instance = lambda g: "%s" % g.label

        self.helper.layout = Layout(
            Accordion(
                AccordionGroup(
                    _('Near Miss Details'),
                    Field('geom', type='hidden', id='nearmisspoint'),
                    Field('personal_involvement', id='nearmiss_personal_involvment'),
                    Field('witness_vehicle', id='nearmiss_witness_vehicle'),
                    Field('date', id='nearmiss_date', template='mapApp/util/%s_datepicker.html', autocomplete='off'),
                    Field('i_type', id='nearmiss_i_type'),
                    Field('incident_with', id='nearmiss_incident_with'),
                    Field('bicycle_type', id='nearmiss_bicycle_type'),
                    Field('ebike', id='nearmiss_ebike'),
                    Field('ebike_class', id='nearmiss_ebike_class'),
                    Field('ebike_speed', id='nearmiss_ebike_speed'),
                    Field('injury', id='nearmiss_injury'),
                    Field('impact', id='nearmiss_impact'),
                    Field('trip_purpose', id='nearmiss_trip_purpose'),
                    Field('details', id='nearmiss_details',placeholder=_('required')),
                ),
                AccordionGroup(
                    _('Conditions'),
                    Field('road_conditions', id='nearmiss_road_conditions'),
                    Field('sightlines', id='nearmiss_sightlines'),
                    Field('cars_on_roadside', id='nearmiss_cars_on_roadside'),
                    Field('bike_lights', id='nearmiss_bike_lights'),
                    Field('terrain', id='nearmiss_terrain'),
                    Field('direction', id='nearmiss_direction'),
                    Field('turning', id='nearmiss_turning'),
                    Field('intersection', id='nearmiss_intersection'),
                    Field('aggressive', id='nearmiss_aggressive'),
                    css_id='nearmiss-conditions',
                ),
                AccordionGroup(
                    _('Personal Details'),
                    HTML(why_personal_link),
                    Div( Div(HTML(why_personal_well), css_class="well"), css_class='why-personal collapse' ),
                    Field('source', id='nearmiss_source'),
                    Field('age', id='nearmiss_age'),
                    Field('birthmonth', id='nearmiss_birthmonth'),
                    InlineCheckboxes('gender', id='nearmiss_gender'),
                    Field('gender_additional', id='nearmiss_gender_additional', rows='1'),
                    Field('regular_cyclist', id='nearmiss_regular_cyclist'),
                    Field('helmet', id='nearmiss_helmet'),
                    css_id='nearmiss-personal-details',
                ),
            )
        )

    def is_valid(self):

        # run default, parent validation first
        valid = super(NearmissForm, self).is_valid()

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
        labels = {
            'gender': _('Please select your gender (choose all that apply)'),
        }
