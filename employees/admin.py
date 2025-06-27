from django.contrib import admin
from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'employee_count', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'department', 'date_of_joining', 'is_active', 'years_of_service']
    list_filter = ['department', 'gender', 'is_active', 'date_of_joining']
    search_fields = ['name', 'email', 'phone_number']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at', 'years_of_service', 'attendance_rate']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone_number', 'address', 'gender')
        }),
        ('Employment Details', {
            'fields': ('department', 'date_of_joining', 'salary', 'is_active')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'years_of_service', 'attendance_rate'),
            'classes': ('collapse',)
        }),
    )
