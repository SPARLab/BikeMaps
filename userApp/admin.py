from django.contrib import admin

from django.contrib.auth import get_user_model
User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ['is_staff']
    list_display = ['username', 'email', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
