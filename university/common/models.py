import uuid

from django.db import models
from django.utils import timezone


class SoftDeletedManager(models.Manager):
    """
    Manager will be excluded deleted objects from queryset
    """
    def get_queryset(self):
        return super().get_queryset().exclude(deleted_at__isnull=False)


class SoftDeleteModelMixin:
    """
    mixin for soft deleted any Model
    expected that this mixin will be applied with a SoftDeletedManager
    """
    deleted_at = models.DateTimeField(null=True, default=None, db_index=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()


class UUIDModel(models.Model):
    """
    default abstract model for custom models
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeletedUUIDModel(SoftDeleteModelMixin, UUIDModel):
    """
    default abstract model with SoftDeleteModelMixin for custom models
    """
    objects = SoftDeletedManager
    all_objects = models.Manager

    class Meta:
        abstract = True
