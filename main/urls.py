from django.urls import path

from main import views


urlpatterns = [
    path('public/', views.PostListAPI.as_view()),
    path('feed/', views.FollowerFeedAPI.as_view()),


]

