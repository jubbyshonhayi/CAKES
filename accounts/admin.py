from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Tenant scope', {'fields': ('school',)}),
    )
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'school')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'school')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('school')
