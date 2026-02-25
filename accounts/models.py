from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    school = models.ForeignKey(
        'schools.School',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='users',
    )

    class Meta:
        indexes = [
            models.Index(fields=['school']),
        ]

    def clean(self):
        super().clean()
        if not self.is_superuser and self.school is None:
            raise ValidationError('Non-superusers must belong to a school.')
        if self.is_superuser and self.school is not None:
            raise ValidationError('Superusers cannot be linked to a school.')

    @property
    def is_school_user(self):
        return not self.is_superuser and self.school is not None
