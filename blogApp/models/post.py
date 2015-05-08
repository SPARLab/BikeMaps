from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from django.db import models

# Create your models here.


##########
# Blog Post class.
# Main class for blog posts.
class Post(models.Model):
    date = models.DateTimeField('Date created', auto_now_add=True)

    title = models.CharField('Title', max_length=100)
    slug = models.SlugField('Slug', unique=True, blank=True, max_length=100)
    published = models.BooleanField('Published', default=False)

    content = models.TextField('Content', blank=True)

    def get_absolute_url(self):
        return reverse('blogApp:view_post', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    # toString()
    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        app_label = 'blogApp'
