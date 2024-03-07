from django.contrib.auth import get_user_model
from django.db import models as _
from django.db.models import functions, Prefetch, Subquery
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics

from main.models import Post
from .serializers import UserSerializer
from users import models
from users.api import serializers

from main.models import Post, Media, PublicTypeChoice

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# https://www.instagram.com/<str: username>/

class ProfileAPI(generics.RetrieveAPIView):
    queryset = models.Profile.profiles.get_profiles()
    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        obj = self.queryset.get(user=self.request.user)
        return obj


class ProfilePublicationAPI(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = serializers.ProfilePublicationSerializer

    def get_queryset(self):
        type_public = PublicTypeChoice.PUBLICATION
        if self.request.path == '/api/profile/reels/':
            type_public = PublicTypeChoice.REELS

        queryset = super().get_queryset().select_related("post")
        queryset = queryset.filter(
            post__profile=self.request.user.profile,
            post__type_public=type_public,
            is_main=True

        )
        return queryset


class ProfileRelevantAPI(generics.ListAPIView):
    queryset = models.RelevantPosts.objects.all()
    serializer_class = serializers.ProfileRelevantSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            Prefetch(
                lookup="history",
                queryset=Post.objects.filter(
                    type_public=PublicTypeChoice.STORY,
                    profile=self.request.user.profile
                ).annotate(
                    media=Subquery(
                        Media.objects.filter(
                            is_main=True,
                            post=_.OuterRef('pk')
                        ).values("media")
                    )
                )
            )
        )
        return queryset


# class ProfilePostsAPI(generics.ListAPIView):
#     queryset = Media.objects.all()
#     serializer_class = serializers.ProfilePostSerializer
#
    # def get_queryset(self):
    #
    #     queryset = super().get_queryset().select_related("post")
    #     queryset = queryset.filter(
    #         post__profile=self.request.user.profile,
    #         is_main=True
    #     )
    #     if self.request.path == 'api/profile/reels/':
    #         return queryset.filter(
    #             post__is_reel=True
    #         )
    #     return queryset


class ProfileSavedAPI(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.ProfileSavedSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (queryset.annotate(
            is_user_in_saved=functions.Coalesce(
                _.Exists(
                    self.request.user.profile.saved_posts.filter(
                        pk=_.OuterRef('pk')
                    )
                ), False
            )
        ).filter(is_user_in_saved=True).annotate(
            media=_.Subquery(
                Media.objects.filter(
                    is_main=True,
                    post=_.OuterRef('pk')
                ).values("media")
            )
        ))
        return queryset

