from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from schools.models import School
from .models import Student


class TenantIsolationTests(TestCase):
    def setUp(self):
        self.school_a = School.objects.create(name='Alpha School', email='alpha@example.com')
        self.school_b = School.objects.create(name='Beta School', email='beta@example.com')

        self.user_a = get_user_model().objects.create_user(
            username='usera',
            password='pass1234',
            school=self.school_a,
        )
        self.user_b = get_user_model().objects.create_user(
            username='userb',
            password='pass1234',
            school=self.school_b,
        )

        self.student_a = Student.objects.create(
            school=self.school_a,
            first_name='Alice',
            last_name='Smith',
            email='alice@alpha.com',
            date_of_birth=date(2010, 5, 15),
            enrollment_number='A-001',
        )

    def test_queryset_for_user_restricts_school(self):
        students = Student.objects.for_user(self.user_b)
        self.assertFalse(students.filter(pk=self.student_a.pk).exists())

    def test_idor_blocked_on_detail_view(self):
        self.client.login(username='userb', password='pass1234')
        response = self.client.get(reverse('student-detail', kwargs={'pk': self.student_a.pk}))
        self.assertEqual(response.status_code, 404)

    def test_school_user_sees_only_own_students(self):
        self.client.login(username='usera', password='pass1234')
        response = self.client.get(reverse('student-list'))
        self.assertContains(response, 'Alice')
