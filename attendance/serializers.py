from rest_framework import serializers
from .models import Attendance
from employees.serializers import EmployeeSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    is_late = serializers.ReadOnlyField()
    working_hours = serializers.ReadOnlyField()
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class AttendanceDetailSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    is_late = serializers.ReadOnlyField()
    working_hours = serializers.ReadOnlyField()
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at') 