from django import forms

from crispy_forms.helper import FormHelper


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