from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'check_in_time', 'check_out_time', 'working_hours']
    list_filter = ['status', 'date', 'employee__department']
    search_fields = ['employee__name', 'employee__department__name']
    ordering = ['-date', 'employee__name']
    readonly_fields = ['created_at', 'updated_at', 'is_late', 'working_hours']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee',)
        }),
        ('Attendance Details', {
            'fields': ('date', 'status', 'check_in_time', 'check_out_time', 'notes')
        }),
        ('Calculated Fields', {
            'fields': ('is_late', 'working_hours'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
