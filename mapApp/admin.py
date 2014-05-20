from django.contrib import admin

# Register your models here.
from mapApp.models import Incident, Person

class PersonStacked(admin.StackedInline):
    model = Person
    verbose_name_plural = "Person"

class IncidentAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
    inlines = [PersonStacked]

#     list_display = ('question', 'pub_date', 'was_published_recently')
    list_filter = ['rep_date']
    
    # search_fields = ['rep_date']

admin.site.register(Incident, IncidentAdmin)