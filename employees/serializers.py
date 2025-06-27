from rest_framework import serializers
from .models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    years_of_service = serializers.ReadOnlyField()
    attendance_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class EmployeeDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    years_of_service = serializers.ReadOnlyField()
    attendance_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class DepartmentDetailSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)
    employee_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Department
        fields = '__all__' 