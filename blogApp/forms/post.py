from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Div
from crispy_forms.layout import Layout, Field, HTML, Button, Submit, Reset

from blogApp.models import Post

class BlogPostForm(forms.ModelForm):
    helper = FormHelper()

    helper.layout = Layout(
        'Create a blog post',
        Field('published'),
        Field('title'),
        Field('content'),
        Div(
            HTML("""
                <div class="btn-group" role="group" aria-label="...">
                  <button type="button" id="italics-btn" class="btn btn-inverse"> <span class="glyphicon glyphicon-italic"></span> </button>
                  <button type="button" id="bold-btn" class="btn btn-inverse"> <span class="glyphicon glyphicon-bold"></span> </button>
                  <button type="button" id="list-btn" class="btn btn-inverse"> <span class="glyphicon glyphicon-list"></span> </button>
                  <button type="button" id="link-btn" class="btn btn-inverse"> <span class="glyphicon glyphicon-link"></span> </button>
                  <button type="button" id="picture-btn" class="btn btn-inverse"> <span class="glyphicon glyphicon-picture"></span> </button>
                </div>
            """),
            css_class="pull-left"
        ),
        Div(
            FormActions(
                Reset('cancel', 'Cancel'),
                Submit('save', 'Save'),
            ),
            css_class="pull-right"
        ),
    )

    class Meta:
        model = Post
        fields = '__all__'
