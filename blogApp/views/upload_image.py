from django.http import JsonResponse
from django.conf import settings

from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST

from PIL import Image
import os

from blogApp.forms import UploadImageForm, BlogPostForm
from  crispy_forms.utils import render_crispy_form

# import logging
# logger = logging.getLogger(__name__)

@user_passes_test(lambda u: u.is_superuser)
@require_POST
def upload_image(request):
    form = UploadImageForm(request.POST, request.FILES)
    if form.is_valid():
        f = request.FILES['image']
        _handle_uploaded_file(f, form.cleaned_data['resize'])

        return JsonResponse({
            'success': True,
            'url': (settings.MEDIA_URL + "blogApp/" + f.name),
            'title': form.cleaned_data['title'],
        })

    else:
        form_html = render_crispy_form(form)
        return JsonResponse({'success': False, 'form_html': form_html})


def _handle_uploaded_file(f, size):
    im = Image.open(f)
    reduction = float(max(im.size)) / float(size)
    im = im.resize(map(lambda x: int(x/reduction), im.size))

    with open(os.path.join(settings.MEDIA_ROOT, "blogApp", f.name), 'wb+') as destination:
        im.save(destination)
