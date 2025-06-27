from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from employees.models import Employee


class Performance(models.Model):
    """Performance model to track employee performance reviews"""
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Below Average'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]

    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='performances'
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_date = models.DateField()
    reviewer = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    areas_for_improvement = models.TextField(blank=True, null=True)
    next_review_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-review_date', 'employee__name']
        indexes = [
            models.Index(fields=['employee']),
            models.Index(fields=['review_date']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.review_date} - Rating: {self.rating}"

    @property
    def rating_text(self):
        """Get the text representation of the rating"""
        return dict(self.RATING_CHOICES)[self.rating]

    @property
    def is_overdue(self):
        """Check if the next review is overdue"""
        from django.utils import timezone
        if self.next_review_date:
            return self.next_review_date < timezone.now().date()
        return False
