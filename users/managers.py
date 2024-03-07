
from django.db import models
from django.db.models import functions as _
from django.utils import timezone
from django.utils.timezone import timedelta

from main.models import Post, PublicTypeChoice


class ProfileManager(models.Manager):

    def get_profiles(self):
        queryset = self.get_queryset()
        queryset = queryset.annotate(
            followers_count=models.Count('followers', distinct=True),
            followings_count=models.Count('followings', distinct=True)
        )
        return queryset.select_related("user")

    def stories(self):
        queryset = self.get_queryset()
        queryset = queryset.annotate(
            story_count=models.Count(
                'posts', filter=models.Q(
                    posts__type_public=PublicTypeChoice.STORY
                ), distinct=True
            )
        ).filter(
            story_count__gt=0, created_at__gt=timezone.now() - timedelta(hours=24)
        ).select_related("user")

        return queryset




