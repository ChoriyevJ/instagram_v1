from django.shortcuts import render
from rest_framework import generics

from main.models import Post, Media, PublicTypeChoice, Comment
from users.models import Profile
from main import serializers

from django.db.models import functions as _, Prefetch, Subquery, OuterRef
from django.db import models


# https://www.instagram.com/
class FollowerFeedAPI(generics.ListAPIView):
    queryset = Profile.profiles.stories()
    serializer_class = serializers.FeedSerializer

    def get_queryset(self):
        queryset = (super().get_queryset().filter(
            models.Q(followings__in=[self.request.user.profile]) |
            models.Q(pk=self.request.user.profile.pk)
        ))

        return queryset


class PostListAPI(generics.ListAPIView):
    queryset = Post.customs.publications().prefetch_related(
        "medias"
    ).select_related("profile__user")
    serializer_class = serializers.PublicationSerializer

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        queryset = queryset.filter(
            profile__followings__in=[self.request.user.profile]
        )
        return queryset



