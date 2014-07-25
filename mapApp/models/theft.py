from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from django.utils import timezone


##########
# Theft class.
#    
class Theft(models.Model):
    pass

    class Meta:
        app_label = 'mapApp'