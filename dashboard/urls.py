from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/department-chart/', views.department_chart_data, name='department_chart_data'),
    path('api/attendance-chart/', views.attendance_chart_data, name='attendance_chart_data'),
    path('api/performance-chart/', views.performance_chart_data, name='performance_chart_data'),
    path('api/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('attendance/', views.attendance_overview, name='attendance_overview'),
] 