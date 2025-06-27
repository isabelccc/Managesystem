from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Employee, Department
from django.contrib.auth import get_user_model

# Create your tests here.

class DepartmentAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.department = Department.objects.create(name='Engineering')

    def test_list_departments(self):
        url = reverse('department-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Engineering', str(response.data))

    def test_create_department(self):
        url = reverse('department-list')
        data = {'name': 'HR'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 2)

class EmployeeAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.department = Department.objects.create(name='Engineering')
        self.employee = Employee.objects.create(
            name='John Doe', email='john@example.com', phone_number='1234567890',
            address='123 Main St', date_of_joining='2023-01-01', department=self.department
        )

    def test_list_employees(self):
        url = reverse('employee-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('John Doe', str(response.data))

    def test_create_employee(self):
        url = reverse('employee-list')
        data = {
            'name': 'Jane Smith', 'email': 'jane@example.com', 'phone_number': '9876543210',
            'address': '456 Elm St', 'date_of_joining': '2023-02-01', 'department': self.department.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
