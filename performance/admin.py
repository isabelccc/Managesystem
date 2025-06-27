from django.contrib import admin
from .models import Performance


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'rating', 'rating_text', 'review_date', 'reviewer', 'is_overdue']
    list_filter = ['rating', 'review_date', 'employee__department']
    search_fields = ['employee__name', 'employee__department__name', 'reviewer']
    ordering = ['-review_date', 'employee__name']
    readonly_fields = ['created_at', 'updated_at', 'rating_text', 'is_overdue']
    date_hierarchy = 'review_date'
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee',)
        }),
        ('Review Details', {
            'fields': ('rating', 'review_date', 'reviewer', 'next_review_date')
        }),
        ('Review Content', {
            'fields': ('comments', 'goals', 'achievements', 'areas_for_improvement')
        }),
        ('Calculated Fields', {
            'fields': ('rating_text', 'is_overdue'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
