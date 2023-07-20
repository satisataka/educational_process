from django.db import models
from django.conf import settings

from university.common.models import SoftDeletedUUIDModel


class Disciplines(SoftDeletedUUIDModel):
    name = models.CharField(max_length=150)
    code = models.PositiveSmallIntegerField(unique=True)
    description = models.TextField(null=True)
    # only Users has role curator
    curator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('name',)


class Specialties(SoftDeletedUUIDModel):
    name = models.CharField(max_length=150)
    code = models.PositiveSmallIntegerField(unique=True)
    description = models.TextField(null=True)

    disciplines = models.ManyToManyField(
        Disciplines,
        related_name='specialties',
        blank=True
    )

    class Meta:
        ordering = ('name',)


class Students(SoftDeletedUUIDModel):
    date_of_admission = models.DateField()
    date_of_expulsion = models.DateField(null=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='student',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('date_of_admission',)


class StudentGroups(SoftDeletedUUIDModel):
    name = models.CharField(max_length=150)

    speciality = models.ForeignKey(
        Specialties,
        related_name='student_groups',
        on_delete=models.PROTECT,
    )
    students = models.ManyToManyField(
        Students,
        related_name='student_groups',
        blank=True,
    )

    class Meta:
        ordering = ('name',)
