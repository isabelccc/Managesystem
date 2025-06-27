from django.db import models
from employees.models import Employee


class Attendance(models.Model):
    """Attendance model to track employee attendance"""
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
    ]

    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='attendances'
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'employee__name']
        unique_together = ['employee', 'date']
        indexes = [
            models.Index(fields=['employee']),
            models.Index(fields=['date']),
            models.Index(fields=['status']),
            models.Index(fields=['employee', 'date']),
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"

    @property
    def is_late(self):
        """Check if employee was late (check-in after 9:00 AM)"""
        if self.check_in_time:
            from datetime import time
            return self.check_in_time > time(9, 0)
        return False

    @property
    def working_hours(self):
        """Calculate working hours if check-in and check-out times are available"""
        if self.check_in_time and self.check_out_time:
            from datetime import datetime, timedelta
            check_in = datetime.combine(self.date, self.check_in_time)
            check_out = datetime.combine(self.date, self.check_out_time)
            duration = check_out - check_in
            return duration.total_seconds() / 3600  # Convert to hours
        return None
