from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from django.db import models
from blogApp.utils import hash62

# Create your models here.


##########
# Blog Post class.
# Main class for blog posts.
class Post(models.Model):
    date = models.DateTimeField('Date created', auto_now_add=True)

    title = models.CharField('Title', max_length=100)
    description = models.CharField('Description', max_length=300)
    slug = models.SlugField('Slug', unique=True, blank=True, max_length=100)
    published = models.BooleanField('Published', default=False)

    content = models.TextField('Content', blank=True)

    def get_absolute_url(self):
        return reverse('blogApp:view_post', kwargs={'slug': self.slug})

    def get_short_url(self):
        return reverse('blogApp:short_url_redirect', kwargs={'s62': hash62.hash(self.id)})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    # toString()
    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        app_label = 'blogApp'
