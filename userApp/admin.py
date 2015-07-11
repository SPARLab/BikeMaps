from django.contrib import admin

from mapApp.admin import HazardAdminsInline
from django.contrib.auth import get_user_model
User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ['is_staff']
    list_display = ['username', 'email', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [
        HazardAdminsInline,
    ]
