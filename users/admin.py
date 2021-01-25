from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_superuser', 'is_staff',  'last_login')
    list_filter = ('is_staff', 'is_superuser')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class SiteAdmins(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name')


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmins)
