from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.urls import reverse

from django.db import models
from blogApp.utils import hash62
from datetime import datetime

# Create your models here.


##########
# Blog Post class.
# Main class for blog posts.
class Post(models.Model):
    LANGUAGE_CHOICES = (
        ('en', _('English')),
        ('fr', _('French'))
    )

    date = models.DateTimeField(_('Date created'), auto_now_add=True)

    title = models.CharField(_('Title'), max_length=100)
    description = models.CharField(_('Description'), max_length=300)
    post_date = models.DateTimeField(_('Date posted'), default=datetime.now)
    slug = models.SlugField(
        _('Slug'), unique=True, blank=True, max_length=100, unique_for_date='date')
    published = models.BooleanField(_('Published'), default=False)
    content = models.TextField(_('Content'), blank=True)
    language = models.CharField(
        _('Language'),
        max_length=50,
        choices=LANGUAGE_CHOICES,
        default='en'
    )


    def get_absolute_url(self):
        return reverse('blogApp:view_post', kwargs={'slug': self.slug})

    def get_short_url(self):
        return reverse('blogApp:short_url_redirect', kwargs={'s62': hash62.hash(self.id)})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    # toString()
    def __unicode__(self):
        return str(self.title)

    def __str__(self):
        return str(self.title)

    class Meta:
        app_label = 'blogApp'
