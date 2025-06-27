from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Department, Employee
from .serializers import (
    DepartmentSerializer, 
    DepartmentDetailSerializer,
    EmployeeSerializer, 
    EmployeeDetailSerializer
)
from django.db import models


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department model with CRUD operations"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DepartmentDetailSerializer
        return DepartmentSerializer

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees in a specific department"""
        department = self.get_object()
        employees = department.employees.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get department statistics"""
        departments = Department.objects.all()
        stats = []
        for dept in departments:
            stats.append({
                'id': dept.id,
                'name': dept.name,
                'employee_count': dept.employee_count,
                'avg_salary': dept.employees.aggregate(
                    avg_salary=models.Avg('salary')
                )['avg_salary'] or 0
            })
        return Response(stats)


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet for Employee model with CRUD operations"""
    queryset = Employee.objects.select_related('department').all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'gender', 'is_active', 'date_of_joining']
    search_fields = ['name', 'email', 'phone_number']
    ordering_fields = ['name', 'date_of_joining', 'salary', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return EmployeeSerializer

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get attendance records for a specific employee"""
        employee = self.get_object()
        from attendance.models import Attendance
        attendances = Attendance.objects.filter(employee=employee).order_by('-date')
        from attendance.serializers import AttendanceSerializer
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        """Get performance records for a specific employee"""
        employee = self.get_object()
        from performance.models import Performance
        performances = Performance.objects.filter(employee=employee).order_by('-review_date')
        from performance.serializers import PerformanceSerializer
        serializer = PerformanceSerializer(performances, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get employee statistics"""
        total_employees = Employee.objects.count()
        active_employees = Employee.objects.filter(is_active=True).count()
        departments = Department.objects.all()
        
        dept_stats = []
        for dept in departments:
            dept_stats.append({
                'department': dept.name,
                'count': dept.employee_count
            })
        
        return Response({
            'total_employees': total_employees,
            'active_employees': active_employees,
            'department_distribution': dept_stats
        })
