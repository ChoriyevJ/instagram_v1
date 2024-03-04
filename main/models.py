from django.core.validators import FileExtensionValidator
from django.db import models

from utils.models import BaseModel


class District(BaseModel):
    title = models.CharField(max_length=31)
    region = models.ForeignKey('self', on_delete=models.CASCADE,
                               related_name='districts', blank=True, null=True)

    def __str__(self):
        return self.title


class Post(BaseModel):
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE,
                                related_name='posts')
    likes = models.ManyToManyField('users.Profile', related_name='liked_posts')

    content = models.CharField(max_length=511, blank=True, null=True)

    is_comment = models.BooleanField(default=True)
    is_show_likes = models.BooleanField(default=True)

    def __str__(self):
        return self.content


class Media(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='medias')
    media = models.FileField(upload_to='post/', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'mp4', 'mpeg', 'avi'])
    ])
    selected_users = models.ManyToManyField('users.Profile', blank=True,
                                            related_name='medias')


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
        return
