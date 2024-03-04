from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.db import models
from utils.models import BaseModel


class User(AbstractUser):
    """
    Default custom user model for My Awesome Project.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class GenderChoice(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female',
    CUSTOM = 'Custom',
    NOT_SAY = 'Not say'


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    followers = models.ManyToManyField('self', blank=True, through="Followers")
    followings = models.ManyToManyField('self', blank=True, through="Followings")

    archive = models.ManyToManyField('ProfileHistory', blank=True)

    about = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=31, choices=GenderChoice.choices,
                              default=GenderChoice.NOT_SAY)
    custom = models.CharField(max_length=31, blank=True, null=True)

    is_private = models.BooleanField(default=False)
    is_recommendation = models.BooleanField(default=True)


class Followers(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_confirm = models.BooleanField(default=True)


class Followings(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_confirm = models.BooleanField(default=True)


class ProfileImage(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to='profile/image/')


class ProfileHistory(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='histories')
    video = models.FileField(upload_to='profile/video/', blank=True, null=True,
                             validators=[FileExtensionValidator(['mp4', 'avi', 'mpeg'])])
    is_active = models.BooleanField(default=True)
