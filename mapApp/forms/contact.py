from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field

class EmailForm(forms.Form):
    helper = FormHelper()
    helper.form_tag = False

    sender = forms.EmailField(
        label = "Email",
        required = True,
        widget=forms.TextInput(attrs={'placeholder':"Enter your email address"})
    )
    
    subject = forms.CharField(
        label = "Subject",
        max_length=100,
        required = False,
        widget=forms.TextInput(attrs={'placeholder': 'What\'s this about?'})
    )
    
    message = forms.CharField(
        label = "Message",
        required = True,
        widget=forms.Textarea(attrs={'placeholder':"Your message here"})
    )
    
    cc_myself = forms.BooleanField(
        label = "Send myself a copy",
        required=False,
        widget=forms.CheckboxInput()
    )

    helper.layout = Layout(
        HTML("""<!-- Modal form -->
                <div class="modal fade" id="emailForm" tabindex="-1" role="dialog" aria-labelledby="emailForm" aria-hidden="false">
                    <div class="modal-dialog">
                        <div class="modal-content">      

                            <div class="modal-header">
                                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                <h4 class="modal-title" id="emailForm">Contact</h4>
                            </div>   

                            <form action="{% url 'mapApp:contact' %}" method="post" role="form">
                                {% csrf_token %}
                                <div class="modal-body">
        """),
        

        Field('sender'),
        Field('subject'),
        Field('message'),
        Field('cc_myself'),
        

        HTML("""                </div>

                                <div class="modal-footer">
                                    <button type="reset" class="btn btn-default" onclick="$('#emailForm').modal('hide');$('.modal-backdrop').hide();">Cancel</button>
                                    <button type="submit" class="btn btn-primary">Send <span class="glyphicon glyphicon-send"></span></button>
                                </div>
                            
                            </form>
                        </div>
                    </div>
                </div>
        """)
    )