from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.db import models
from utils.models import BaseModel

from users import managers


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
    followers = models.ManyToManyField('self', symmetrical=False, blank=True,
                                       related_name="followings")
    confirms = models.ManyToManyField('self', symmetrical=False, blank=True,
                                      through="Confirms")

    about = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=31, choices=GenderChoice.choices,
                              default=GenderChoice.NOT_SAY)
    custom = models.CharField(max_length=31, blank=True, null=True)

    image = models.ImageField(upload_to='profile/images/', blank=True, null=True)

    publication_count = models.PositiveIntegerField(default=0)

    is_private = models.BooleanField(default=False)
    is_recommendation = models.BooleanField(default=True)

    profiles = managers.ProfileManager()
    objects = models.Manager()

    def __str__(self):
        return self.user.username


class Confirms(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name="confirm_followers")
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                 related_name="confirm_profiles")
    is_confirm = models.BooleanField(default=True)
    is_closer = models.BooleanField(default=False)


class RelevantPosts(BaseModel):
    title = models.CharField(max_length=31)
    history = models.ManyToManyField('main.Post',
                                     related_name='profiles')




