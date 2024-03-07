from django.core.validators import FileExtensionValidator
from django.db import models

from utils.models import BaseModel

from main import managers


class PublicTypeChoice(models.TextChoices):
    PUBLICATION = 'Publication'
    STORY = 'Story'
    REELS = 'reels'


class Region(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Place(BaseModel):
    title = models.CharField(max_length=31)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,
                               related_name='districts', blank=True, null=True)

    def __str__(self):
        return self.title


class Post(BaseModel):
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE,
                                related_name='posts')
    place = models.ForeignKey(Place, on_delete=models.CASCADE,
                              related_name='posts', blank=True, null=True)

    likes = models.ManyToManyField('users.Profile', related_name='liked_posts', blank=True)
    saved = models.ManyToManyField('users.Profile', related_name='saved_posts', blank=True)
    watchers = models.ManyToManyField('users.Profile', related_name="watching_posts", blank=True)

    content = models.CharField(max_length=511, blank=True, null=True)

    type_public = models.CharField(max_length=31,
                                   choices=PublicTypeChoice.choices)

    number_of_comments = models.PositiveIntegerField(default=0)
    number_of_likes = models.PositiveIntegerField(default=0)

    is_show_comment = models.BooleanField(default=True)
    is_show_likes = models.BooleanField(default=True)

    objects = models.Manager()
    customs = managers.PostAndReelsManager()

    def __str__(self):
        return f'Post(pk={self.pk})'


class Media(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='medias')
    media = models.FileField(upload_to='post/', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'mp4', 'mpeg', 'avi'])
    ])
    selected_users = models.ManyToManyField('users.Profile', blank=True,
                                            related_name='medias')
    is_main = models.BooleanField(default=False)


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    owner = models.ForeignKey('users.Profile', on_delete=models.CASCADE,
                              related_name='comments')
    likes = models.ManyToManyField('users.Profile', related_name='liked_comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               related_name='children')

    content = models.CharField(max_length=511)

    def __str__(self):
        return f'Comment(pk={self.pk}), content="{self.content}"'

    def __repr__(self):
        return f'Comment(pk={self.pk}), content="{self.content}"'
