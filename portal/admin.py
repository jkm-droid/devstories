from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Story, UserProfile


class CustomStory(admin.ModelAdmin):
    list_display = ('title', 'author', 'image_tag', 'likes', 'smiles', 'views', 'is_saved', 'draft', 'created_on')


class CustomUserProfile(admin.ModelAdmin):

    list_display = ('user', 'status', 'is_online', 'description', 'image_tag', 'is_profile', 'created_on')


admin.site.register(Story, CustomStory)
admin.site.register(UserProfile, CustomUserProfile)
admin.site.site_title = 'Developer Stories'
admin.site.index_title = 'DeveloperStories Admin'
admin.site.site_header = 'Developer Stories'
