from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div
from crispy_forms.bootstrap import Accordion, AccordionGroup

from mapApp.models import Theft
import datetime

why_personal_link = format_lazy('<a class="text-info" data-toggle="collapse" aria-expanded="false" aria-controls="why-personal" href=".tab-pane.active .why-personal"><span class="glyphicon glyphicon-question-sign"></span> <strong>{why}</strong></a>', why=_("Why are we asking for personal details?"))

why_personal_well = _("Personal details such as age and gender are routinely collected in health research including studies examining cycling injuries (e.g., Cripton et al. 2015). In addition, details such as rider experience and gender have been shown to be important predictors of cycling safety and risk (Beck et al. 2007). The goal of BikeMaps.org is to gather more comprehensive data to better assess cycling safety and risk. Providing personal details will allow us to more accurately fill in these data gaps.")


class TheftForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False # removes auto-inclusion of form tag in template
        self.helper.disable_csrf = True

        self.fields['police_report'].required = False
        self.fields['insurance_claim'].required = False

        self.helper.layout = Layout(
                Accordion(
                    AccordionGroup(
                    _('Theft Details'),
                    Field('geom', type='hidden', id='theftPoint'),
                    Field('date', id='theft_date', template='mapApp/util/%s_datepicker.html', autocomplete='off'),
                    Field('i_type', id='theft_i_type'),
                    Field('how_locked', id='theft_how_locked'),
                    Field('lock', id='theft_lock'),
                    Field('locked_to', id='theft_locked_to'),
                    Field('lighting', id='theft_lighting'),
                    Field('traffic', id='theft_traffic'),
                    Field('details', id='theft_details', placeholder=_('required')),
                ),
                AccordionGroup(
                    _('Personal Details'),
                    HTML(why_personal_link),
                    Div( Div(HTML(why_personal_well), css_class="well"), css_class='why-personal collapse' ),
                    Field('source', id='theft_source'),
                    Field('regular_cyclist', id='theft_regular_cyclist'),
                    Field('police_report', id='theft_police_report'),
                    Field('police_report_num', id='theft_police_report_num'),
                    Field('insurance_claim', id='theft_insurance_claim'),
                    Field('insurance_claim_num', id='theft_insurance_claim_num'),
                    css_id='theft-personal-details',
                ),
            )
        )

    def is_valid(self):

        # run default, parent validation first
        valid = super(TheftForm, self).is_valid()

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
        model = Theft
        exclude = ['p_type']
