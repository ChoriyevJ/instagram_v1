from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import User as UserType
from users import models
from main.models import Post, Media

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField()
    followings_count = serializers.IntegerField()
    username = serializers.SerializerMethodField()
    image = serializers.CharField()

    class Meta:
        model = models.Profile
        fields = (
            'username', 'publication_count',
            'followers_count', 'followings_count',
            'image',

        )

    def get_username(self, obj):
        return obj.user.username


class ProfilePublicationSerializer(serializers.ModelSerializer):
    number_of_comments = serializers.StringRelatedField(source="post.number_of_comments")
    number_of_likes = serializers.StringRelatedField(source="post.number_of_likes")

    class Meta:
        model = Media
        fields = ('media', 'number_of_comments', 'number_of_likes')


class HistorySerializer(serializers.ModelSerializer):
    media = serializers.CharField()

    class Meta:
        model = Post
        fields = ('media',)


class ProfileRelevantSerializer(serializers.ModelSerializer):

    history = HistorySerializer(many=True)

    class Meta:
        model = models.RelevantPosts
        fields = ('title', 'history')


class ProfileSavedSerializer(serializers.ModelSerializer):
    media = serializers.CharField()

    class Meta:
        model = Post
        fields = ('media',)



