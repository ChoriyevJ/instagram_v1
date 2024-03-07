from rest_framework import serializers

from main import models
from users.models import Profile


# class ProfileImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProfileImage
#         fields = ('image',)


class FeedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    image = serializers.CharField()
    is_watched = serializers.BooleanField()

    # images = ProfileImageSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('username', "image", "is_watched")

    def get_username(self, obj):
        return obj.user.username


class PublicationMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = ('media',)


class PublicationSerializer(serializers.ModelSerializer):

    medias = PublicationMediaSerializer(many=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = (
            'username', 'medias', 'created_at', 'content',
        )

    def get_username(self, obj):
        print('\n\n')
        print(obj)
        print('\n\n')
        return obj.profile.user.username

