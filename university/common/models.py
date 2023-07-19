import uuid

from django.db import models


class ExcludeDeletedManagerMixin:
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class DefaultManager(ExcludeDeletedManagerMixin, models.Manager):
    pass


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = DefaultManager
    all_objects = models.Manager

    class Meta:
        abstract = True
