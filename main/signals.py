from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Post, Media, PublicTypeChoice


@receiver(post_save, sender=Post)
def change_to_reel(sender, instance, created, **kwargs):
    if created:
        if instance.type_public in (PublicTypeChoice.REELS, PublicTypeChoice.PUBLICATION):
            instance.profile.publication_count += 1
            instance.profile.save()
        else:
            instance.is_show_comment = False
            instance.is_show_likes = False
            instance.save()





