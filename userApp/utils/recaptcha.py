from django.conf import settings
import requests

class ReCaptcha:
    def __init__(self, request):
        params = {
            'secret': settings.RECAPTCHA_SECRET,
            'response': request.POST.get('g-recaptcha-response'),
            'remoteip': request.META['REMOTE_ADDR']
        }
        self.response = requests.get('https://www.google.com/recaptcha/api/siteverify', params=params).json()

    def is_valid(self):
        return self.response['success']
