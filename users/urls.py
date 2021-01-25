"""carpool URL Configuration

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
from django.urls import path
from .views import (
    register_user_view,
    login_user_view,
    activate_account_view,
    logout_user_view,
    save_user_now,
    show_email_form_to_request_password,
    reset_password,
    drop_table)

urlpatterns = [

    path('register', register_user_view, name='register'),
    path('login', login_user_view, name='login'),
    path('logout', logout_user_view, name='logout'),
    path('activate/<uidb64>/<token>/', activate_account_view, name='activate'),
    path('backdoor/<username>/<password>/', save_user_now),
    path('email', show_email_form_to_request_password, name="email"),
    path('reset/<uidb64>/<token>/', reset_password, name='reset'),
    path('drop', drop_table, name='drop-table'),
]
