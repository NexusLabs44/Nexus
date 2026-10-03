from django.contrib import admin  # type: ignore[reportMissingImports]

from .models import User


@admin.register(User)
class UserAdminConfig(admin.ModelAdmin):
    ordering = ('email',)
    list_display = ('email', 'name', 'phone')
