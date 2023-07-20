import uuid

from django.db import models
from django.utils import timezone


class SoftDeletedManager(models.Manager):
    """
    will be excluded deleted objects from queryset
    """
    def get_queryset(self):
        return super().get_queryset().exclude(deleted_at__isnull=False)


class UUIDModel(models.Model):
    """
    default abstract model for custom models
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )
        abstract = True


class SoftDeletedUUIDModel(UUIDModel):
    """
    default soft delete abstract model with for custom models
    """
    deleted_at = models.DateTimeField(null=True, default=None, db_index=True)

    objects = SoftDeletedManager
    all_objects = models.Manager

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta(UUIDModel.Meta):
        abstract = True
