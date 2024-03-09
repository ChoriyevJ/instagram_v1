from django.db import models


from main import models as main_models


class PostAndReelsManager(models.Manager):

    def publications(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(
            type_public=main_models.PublicTypeChoice.STORY
        )
        return queryset

    def stories(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            type_public=main_models.PublicTypeChoice.STORY
        )
        return queryset





