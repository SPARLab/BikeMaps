from django.contrib.gis.db import models

class Gender(models.Model):
    value = models.CharField(
        blank=False,
        max_length=10,
    )

    label = models.CharField(
        blank=False,
        max_length=50,
    )
    
    def __str__(self):
         return self.value
