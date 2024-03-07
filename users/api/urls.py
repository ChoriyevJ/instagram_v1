from django.urls import path

from users.api import views

urlpatterns = [
    path("", views.ProfileAPI.as_view()),
    path("posts/", views.ProfilePublicationAPI.as_view()),
    path("reels/", views.ProfilePublicationAPI.as_view()),
    path('relevant/', views.ProfileRelevantAPI.as_view()),


]
