from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


# https://clck.ru/rauHe
@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'email', 'last_name', 'first_name', 'patronymic', 'total_points')
    list_display_links = ('id', 'username', 'email', 'last_name', 'first_name', 'patronymic')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'patronymic', 'email', 'total_points')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('username', 'last_name', 'first_name', 'patronymic')
    readonly_fields = ('total_points',)
    save_on_top = True
