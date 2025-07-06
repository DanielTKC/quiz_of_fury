"""
URL configuration for quiz_of_fury project.
"""
from django.contrib import admin
from django.urls import path, include
from quiz.views import profile_view
from django.shortcuts import redirect


urlpatterns = [
    path('', include('quiz.urls')),  # Redirect root URL to quiz app
    path('admin/', admin.site.urls),
    path("accounts/profile/", profile_view, name="account_profile"),
    path("accounts/", include('allauth.urls')),
]
