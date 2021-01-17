#-*- coding: utf-8 -*-

import re

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    # almost verbatim copy from the auth user model
    # adds username(db_index=True), email(unique=True, blank=False, max_length=254)
    username = models.CharField(_("username"), max_length=30, unique=True, db_index=True,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters'),
                                validators=[
                                    validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'),
                                                              'invalid')
                                ])
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    email = models.EmailField(_("email"), max_length=254, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse('spirit:profile-detail', kwargs={'pk': self.pk,
                                                        'slug': self.slug})

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email, ])


class User(AbstractUser):

    class Meta:
        app_label = 'spirit'
        ordering = ['-date_joined', ]
        verbose_name = _('user')
        verbose_name_plural = _('users')
