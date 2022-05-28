from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
# from django.utils.translation import ugettext_lazy as _
from .models import User
# from related_admin import RelatedFieldAdmin


class UserAdmin(DjangoUserAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Main', {'fields': ('email', 'password', 'verified')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'address', 'avatar',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'verified'),
        }),
    )
    list_display = ('email', 'get_fullname', 'is_staff', 'date_joined', 'verified', 'created_at')
    search_fields = ('phone', 'first_name', 'last_name', 'username',)
    ordering = ('id',)
    list_filter = (
        'verified', 'is_active', 'is_staff', 'is_superuser',
    )

    @staticmethod
    def get_fullname(obj):
        return "{} {}".format(obj.first_name, obj.last_name)


admin.site.register(User, UserAdmin)