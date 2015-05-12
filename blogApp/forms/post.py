from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Div
from crispy_forms.layout import Layout, Field, HTML, Button, Submit, Reset

from blogApp.models import Post

class BlogPostForm(forms.ModelForm):
    helper = FormHelper()
    # helper.form_tag = False

    helper.layout = Layout(
        'Create a blog post',
        Field('published'),
        Field('title'),
        Field('content'),
        Div(
            HTML("""
                <div class="btn-group" role="group" aria-label="...">
                  <button type="button" id="italics-btn" title="Insert italics code" class="btn btn-inverse"> <span class="glyphicon glyphicon-italic"></span> </button>
                  <button type="button" id="bold-btn" title="Insert bold text code" class="btn btn-inverse"> <span class="glyphicon glyphicon-bold"></span> </button>
                  <button type="button" id="list-btn" title="Insert a list item" class="btn btn-inverse"> <span class="glyphicon glyphicon-list"></span> </button>
                  <button type="button" id="link-btn" title="Insert a link" class="btn btn-inverse"> <span class="glyphicon glyphicon-link"></span> </button>
                  <button type="button" id="picture-btn" title="Upload picture" class="btn btn-inverse" data-toggle="modal" data-target="#upload-img-modal"> <span class="glyphicon glyphicon-picture"></span> </button>
                </div>
            """),
            css_class="pull-left"
        ),
        Div(
            FormActions(
                Submit('save', 'Save'),
            ),
            css_class="pull-right"
        ),
    )

    class Meta:
        model = Post
        fields = '__all__'
