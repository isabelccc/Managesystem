from rest_framework import serializers
from .models import Performance
from employees.serializers import EmployeeSerializer


class PerformanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    rating_text = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Performance
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class PerformanceDetailSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    rating_text = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Performance
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at') 