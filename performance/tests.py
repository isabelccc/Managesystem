from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from employees.models import Employee, Department
from .models import Performance
from django.contrib.auth import get_user_model

# Create your tests here.

class PerformanceAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.department = Department.objects.create(name='Engineering')
        self.employee = Employee.objects.create(
            name='John Doe', email='john@example.com', phone_number='1234567890',
            address='123 Main St', date_of_joining='2023-01-01', department=self.department
        )
        self.performance = Performance.objects.create(
            employee=self.employee, rating=4, review_date='2023-06-01'
        )

    def test_list_performance(self):
        url = reverse('performance-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('John Doe', str(response.data))

    def test_create_performance(self):
        url = reverse('performance-list')
        data = {
            'employee': self.employee.id, 'rating': 5, 'review_date': '2023-06-02'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Performance.objects.count(), 2)
