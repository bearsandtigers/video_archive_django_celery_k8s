from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from video_archive.storage_backends import (
    OriginalMediaStorage,
    PublicMediaStorage
)
from App.utils import generate_id

#uploaded_at = models.DateTimeField(auto_now_add=True)

class Clip(models.Model):
    hash_id = models.CharField(max_length=50)
    link = models.CharField(max_length=350, default=False, null=True)
    original_name = models.CharField(max_length=150, default=None, null=True)
    original_file = models.FileField(storage=OriginalMediaStorage(), default=None, null=True)
    thumbnail_file = models.FileField(storage=PublicMediaStorage(), default=None, null=True)
    mp4_file = models.FileField(storage=PublicMediaStorage(), default=None, null=True)

    def __str__(self):
        return f'{self.id}, {self.hash_id}, {self.original_name}'

    def save(self, *args, **kwargs):
        super(Clip, self).save(*args, **kwargs)
        return self

@receiver(pre_save, sender=Clip)
def generate_hash_id(sender, instance, **kwargs):
    instance.hash_id = generate_id(
        f'{instance.link}{instance.original_name}')
