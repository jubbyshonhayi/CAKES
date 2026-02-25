from django.core.exceptions import ValidationError
from django.db import models


class StudentQuerySet(models.QuerySet):
    def for_user(self, user):
        if getattr(user, 'is_superuser', False):
            return self.none()
        school_id = getattr(user, 'school_id', None)
        if school_id is None:
            return self.none()
        return self.filter(school_id=school_id)


class Student(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.PROTECT, related_name='students')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    date_of_birth = models.DateField()
    enrollment_number = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StudentQuerySet.as_manager()

    class Meta:
        ordering = ['last_name', 'first_name']
        constraints = [
            models.UniqueConstraint(fields=['school', 'email'], name='uniq_student_email_per_school'),
            models.UniqueConstraint(fields=['school', 'enrollment_number'], name='uniq_enrollment_per_school'),
        ]
        indexes = [
            models.Index(fields=['school', 'last_name', 'first_name']),
            models.Index(fields=['school', 'enrollment_number']),
            models.Index(fields=['school', 'email']),
        ]

    def clean(self):
        if self.school_id is None:
            raise ValidationError('Student must belong to a school.')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
