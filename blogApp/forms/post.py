from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_lazy as trans
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Div
from crispy_forms.layout import Layout, Field, HTML, Button, Submit, Reset

from blogApp.models import Post

class BlogPostForm(forms.ModelForm):
    helper = FormHelper()
    # helper.form_tag = False

    helper.layout = Layout(
        _('Create a blog post'),
        Field('published'),
        Field('title'),
        Field('description'),
        Field('post_date'),
        Field('content'),
        Div(
            HTML("""
                <div class="btn-group" role="group" aria-label="...">
                  <button type="button" id="italics-btn" title="{0}" class="btn btn-inverse"> <span class="glyphicon glyphicon-italic"></span> </button>
                  <button type="button" id="bold-btn" title="{1}" class="btn btn-inverse"> <span class="glyphicon glyphicon-bold"></span> </button>
                  <button type="button" id="list-btn" title="{2}" class="btn btn-inverse"> <span class="glyphicon glyphicon-list"></span> </button>
                  <button type="button" id="link-btn" title="{3}" class="btn btn-inverse"> <span class="glyphicon glyphicon-link"></span> </button>
                  <button type="button" id="picture-btn" title="{4}" class="btn btn-inverse" data-toggle="modal" data-target="#upload-img-modal"> <span class="glyphicon glyphicon-picture"></span> </button>
                </div>
            """.format(trans("Insert italics code"), trans("Insert bold text code"), trans("Insert a list item"), trans("Insert a link"), trans("Upload picture"))),
            css_class="pull-left"
        ),
        Div(
            FormActions(
                Submit('save', _('Save')),
            ),
            css_class="pull-right"
        ),
    )

    class Meta:
        model = Post
        fields = '__all__'
