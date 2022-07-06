import os
import re
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey 
from django.db import models
from django.db.models import QuerySet

from core.models import TimeStampMixin, User, HashTagMixin


class PostMixin(object):
    def following(self, user: User):
        query = models.Q(user__in=user.following.all())
        query |= models.Q(user=user)
        return self.filter(query)
    
    def filter_is_active(self):
        query = models.Q(user__is_active=True)
        query &= models.Q(is_active=True)
        return self.filter(query)

class PostQuerySet(QuerySet, PostMixin):
    pass


class PostManager(models.Manager, PostMixin):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)


def upload_to_user_dir(instance, filename):
    return os.path.join(instance.user.username, filename)


class Post(HashTagMixin, TimeStampMixin):
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_to_user_dir, blank=True, null=True)
    user = models.ForeignKey(
        "core.User", 
        on_delete=models.CASCADE,
        related_name="posts",
        blank=False, null=False,
    )
    is_active = models.BooleanField(default=True)

    objects = PostManager()

    def __str__(self) -> str:
        return f"Post {self.id} by user {self.user}"

    class Meta:
        ordering = ("-created_at", "-id")


class HashTag(TimeStampMixin):
    text = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"Hashtag {self.text}"
    