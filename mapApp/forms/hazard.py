from django.utils.translation import ugettext_lazy as _
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div
from crispy_forms.bootstrap import Accordion, AccordionGroup

from mapApp.models import Hazard

why_personal_link = u'<a class="text-info" data-toggle="collapse" aria-expanded="false" aria-controls="why-personal" href=".tab-pane.active .why-personal"><span class="glyphicon glyphicon-question-sign"></span> <strong>%(question)s</strong></a>' % {'question': _(u"Why are we asking for personal details?")}

why_personal_well = _(u"Personal details such as age and gender are routinely collected in health research including studies examining cycling injuries (e.g., Cripton et al. 2015). In addition, details such as rider experience and gender have been shown to be important predictors of cycling safety and risk (Beck et al. 2007). The goal of BikeMaps.org is to gather more comprehensive data to better assess cycling safety and risk. Providing personal details will allow us to more accurately fill in these data gaps.")


class HazardForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False # removes auto-inclusion of form tag in template
    helper.disable_csrf = True

    helper.layout = Layout(
        Accordion(
            AccordionGroup(
                _('Hazard Details'),
                Field('geom', type='hidden', id='hazPoint'),
                Field('date', id='hazard_date', template='mapApp/util/datepicker.html', autocomplete='off'),
                Field('hazard_category', id='hazard-category'),
                Field('i_type', id='hazard-type'),
            ),
            AccordionGroup(
                _('Description'),
                Field('details', placeholder=_('optional')),
                css_id='hazard-description',
            ),
            AccordionGroup(
                _('Personal Details'),
                HTML(why_personal_link),
                Div( Div(HTML(why_personal_well), css_class="well"), css_class='why-personal collapse' ),
                Field('age'),
                Field('birthmonth'),
                Field('sex'),
                Field('regular_cyclist'),
                css_id='hazard-personal-details',
            ),
        )
    )

    class Meta:
        model = Hazard
        exclude = ['p_type', 'hazard_fixed', 'expires_date']
