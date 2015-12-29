from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div
from crispy_forms.bootstrap import Accordion, AccordionGroup

from mapApp.models import Incident

why_personal_link = string_concat('<a class="text-info" data-toggle="collapse" aria-expanded="false" aria-controls="why-personal" href=".tab-pane.active .why-personal"><span class="glyphicon glyphicon-question-sign"></span> <strong>', _(u"Why are we asking for personal details?"), '</strong></a>')

why_personal_well = _(u"Personal details such as age and gender are routinely collected in health research including studies examining cycling injuries (e.g., Cripton et al. 2015). In addition, details such as rider experience and gender have been shown to be important predictors of cycling safety and risk (Beck et al. 2007). The goal of BikeMaps.org is to gather more comprehensive data to better assess cycling safety and risk. Providing personal details will allow us to more accurately fill in these data gaps.")


class NearmissForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template
    helper.disable_csrf = True

    helper.layout = Layout(
        Accordion(
            AccordionGroup(
                _('Incident Details'),
                Field('geom', type='hidden', id='nearmisspoint'),
                Field('date', id='nearmiss_date', template='mapApp/util/%s_datepicker.html', autocomplete='off'),
                Field('i_type'),
                Field('incident_with'),
                Field('injury'),
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
                css_id='incident-conditions',
            ),
            AccordionGroup(
                _('Description'),
                Field('details', placeholder=_('optional')),
                css_id='incident-description',
            ),
            AccordionGroup(
                _('Personal Details'),
                HTML(why_personal_link),
                Div( Div(HTML(why_personal_well), css_class="well"), css_class='why-personal collapse' ),
                Field('age'),
                Field('birthmonth'),
                Field('sex'),
                Field('regular_cyclist'),
                Field('helmet'),
                Field('intoxicated'),
                css_id='incident-personal-details',
            ),
        )
    )

    class Meta:
        model = Incident
        exclude = ['p_type']
