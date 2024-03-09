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
        ).annotate(
            is_watched=_.Coalesce(
                models.Exists(
                    self.request.user.profile.watching_posts.filter(
                        profile=OuterRef('pk')
                    )
                ), False
            )
        ))

        return queryset


class PostListAPI(generics.ListAPIView):
    queryset = Post.customs.publications().prefetch_related(
        "medias"
    ).select_related("profile__user", "profile")
    serializer_class = serializers.PublicationSerializer

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        queryset = (queryset.filter(
            profile__followings__in=[self.request.user.profile]
        ))

        return queryset


class MainPostsReelsListAPI(generics.ListAPIView):
    queryset = Post.customs.publications().select_related(
        "profile__user"
    ).prefetch_related(
        "medias"
    )
    serializer_class = serializers.MainPostsReelsListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            models.Q(profile__followings__in=[self.request.user.profile]) |
            models.Q(profile__user=self.request.user)
        ).annotate(
            username=models.F("profile__user__username"),
            image=models.F("profile__image"),
            is_liked=models.Case(
                models.When(
                    likes__user=self.request.user, then=True
                ),
                default=False,
                output_field=models.BooleanField()
            ),
            is_saved=models.Case(
                models.When(
                    saved__user=self.request.user, then=True
                ),
                default=False,
                output_field=models.BooleanField()
            ),
            likes_count=models.Count(
                'likes', distinct=True
            ),
            is_show_story=Subquery(
                Post.customs.stories().filter(
                    profile=OuterRef('profile')
                ).annotate(
                    is_watched=models.Case(
                        models.When(
                            watchers__user=self.request.user, then=True
                        ),
                        default=False,
                        output_field=models.BooleanField()
                    )
                ).values("is_watched")
            ),

        ).order_by("-created_at")

        return queryset
















