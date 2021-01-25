"""devstories URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    index_view,
    write_story_view,
    dashboard_view,
    edit_story_view,
    full_story_view,
    delete_story_view,
    settings_profile_view,
    drafted_stories_view,
    tagged_stories_view,
    like_view,
    smile_view,
    register_user_views,
    search_view,
    deactivate_users_account,
    save_story_for_later_view,
    reading_list_view,
    check_saved_status,
    get_notification_view
)


urlpatterns = [
    path('', index_view, name="portal"),
    path('writestory/', write_story_view, name="writestory"),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('draftedstories', drafted_stories_view, name="draftedstories"),
    path('taggedstories/<str:slug>', tagged_stories_view, name="taggedstories"),
    path('reading_list', reading_list_view, name="readinglist"),
    path('settings', settings_profile_view, name="settings"),
    path('<int:id>/edit/', edit_story_view),
    path('delete/<str:slug>', delete_story_view),
    path('<str:slug>', full_story_view, name="fullstory"),
    path('<int:story_id>/preference/<int:userpreference>', like_view, name="like"),
    path('<int:story_id>/smile/<int:userpreference>', smile_view, name="smile"),
    path('<int:story_id>/userviews/<int:userview>', register_user_views, name='userviews'),
    path('search/', search_view, name="search"),
    path('deactivate/', deactivate_users_account, name='deactivate'),
    path('<int:story_id>/save/<int:usersave>', save_story_for_later_view, name="save"),
    path('<int:story_id>/status/', check_saved_status, name="status"),
    path('notifications/', get_notification_view, name='notifications'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
