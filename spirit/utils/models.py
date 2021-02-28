#-*- coding: utf-8 -*-

from django.db.models.fields import SlugField
from django.utils.text import slugify
from six import smart_text


class AutoSlugField(SlugField):
    """
    Auto populates itself from another field.

    It behaves like a regular SlugField.
    When populate_from is provided it'll populate itself on creation
    only if a slug was not provided.
    """
    def __init__(self, *args, **kwargs):
        self.populate_from = kwargs.pop('populate_from', None)
        super(AutoSlugField, self).__init__(*args, **kwargs)

    def pre_save(self, instance, add):
        default = super(AutoSlugField, self).pre_save(instance, add)

        if default or not add or not self.populate_from:
            return default

        value = getattr(instance, self.populate_from)

        if value is None:
            return default

        slug = slugify(smart_text(value))[:self.max_length].strip('-')

        # Update the model’s attribute
        setattr(instance, self.attname, slug)

        return slug

    # def deconstruct(self):
        # TODO: django 1.7 requires this
