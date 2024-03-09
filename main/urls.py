from django.urls import path

from main import views


urlpatterns = [
    # path('posts/', views.PostListAPI.as_view()),
    path('list/', views.MainPostsReelsListAPI.as_view()),
    path('feed/', views.FollowerFeedAPI.as_view()),


]

