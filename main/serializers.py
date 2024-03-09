from rest_framework import serializers

from main import models
from users.models import Profile


class FeedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    image = serializers.CharField()
    is_watched = serializers.BooleanField()

    # images = ProfileImageSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "username",
            "image",
            "is_watched",
        )

    def get_username(self, obj):
        return obj.user.username


class PublicationMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = ('media',)


class PublicationSerializer(serializers.ModelSerializer):

    medias = PublicationMediaSerializer(many=True)
    username = serializers.SerializerMethodField()
    image = serializers.StringRelatedField(source="profile.image", read_only=True)
    is_watched = serializers.BooleanField()

    class Meta:
        model = models.Post
        fields = (
            'username', "image", 'is_watched', 'medias', 'created_at', 'content',
        )

    def get_username(self, obj):
        return obj.profile.user.username


class MainPostsReelsListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    image = serializers.CharField(read_only=True)
    is_show_story = serializers.BooleanField(read_only=True)

    medias = PublicationMediaSerializer(many=True, read_only=True)
    is_liked = serializers.BooleanField()
    likes_count = serializers.IntegerField(read_only=True)
    is_saved = serializers.BooleanField()

    class Meta:
        fields = (
            'username',
            'image',
            'is_show_story',

            'medias',
            'content',
            'type_public',

            'is_show_comment',
            'is_show_likes',
            'is_liked',
            'is_saved',

            'likes_count',
        )
        extra_kwargs = {
            'content': {'read_only': True}
        }
        model = models.Post











