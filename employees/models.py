from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone


class Department(models.Model):
    """Department model for organizing employees"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def employee_count(self):
        return self.employees.count()


class Employee(models.Model):
    """Employee model with all required fields"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    date_of_joining = models.DateField()
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        related_name='employees'
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['department']),
            models.Index(fields=['date_of_joining']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} - {self.department.name}"

    @property
    def years_of_service(self):
        """Calculate years of service"""
        today = timezone.now().date()
        return (today - self.date_of_joining).days // 365

    @property
    def attendance_rate(self):
        """Calculate attendance rate for the current month"""
        from attendance.models import Attendance
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        total_days = Attendance.objects.filter(
            employee=self,
            date__month=current_month,
            date__year=current_year
        ).count()
        
        present_days = Attendance.objects.filter(
            employee=self,
            date__month=current_month,
            date__year=current_year,
            status='present'
        ).count()
        
        if total_days == 0:
            return 0
        return (present_days / total_days) * 100
