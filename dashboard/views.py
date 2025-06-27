from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg
from employees.models import Department, Employee
from attendance.models import Attendance
from performance.models import Performance
from django.utils import timezone
from datetime import datetime, timedelta


def dashboard(request):
    """Main dashboard view"""
    return render(request, 'dashboard/dashboard.html')


def department_chart_data(request):
    """API endpoint for department employee count chart"""
    departments = Department.objects.annotate(
        employee_count=Count('employees')
    ).values('name', 'employee_count')
    
    data = {
        'labels': [dept['name'] for dept in departments],
        'data': [dept['employee_count'] for dept in departments],
        'backgroundColor': [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
            '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
        ]
    }
    
    return JsonResponse(data)


def attendance_chart_data(request):
    """API endpoint for monthly attendance overview chart"""
    # Get current month data
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    # Get daily attendance counts for the current month
    daily_stats = []
    start_date = datetime(current_year, current_month, 1).date()
    
    if current_month == 12:
        end_date = datetime(current_year + 1, 1, 1).date() - timedelta(days=1)
    else:
        end_date = datetime(current_year, current_month + 1, 1).date() - timedelta(days=1)
    
    current_date = start_date
    while current_date <= end_date:
        # Skip weekends
        if current_date.weekday() < 5:
            day_attendances = Attendance.objects.filter(date=current_date)
            daily_stats.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'present': day_attendances.filter(status='present').count(),
                'absent': day_attendances.filter(status='absent').count(),
                'late': day_attendances.filter(status='late').count(),
                'total': day_attendances.count()
            })
        current_date += timedelta(days=1)
    
    # Prepare data for chart
    dates = [stat['date'] for stat in daily_stats]
    present_data = [stat['present'] for stat in daily_stats]
    absent_data = [stat['absent'] for stat in daily_stats]
    late_data = [stat['late'] for stat in daily_stats]
    
    data = {
        'labels': dates,
        'datasets': [
            {
                'label': 'Present',
                'data': present_data,
                'backgroundColor': '#4BC0C0',
                'borderColor': '#4BC0C0',
                'borderWidth': 1
            },
            {
                'label': 'Absent',
                'data': absent_data,
                'backgroundColor': '#FF6384',
                'borderColor': '#FF6384',
                'borderWidth': 1
            },
            {
                'label': 'Late',
                'data': late_data,
                'backgroundColor': '#FFCE56',
                'borderColor': '#FFCE56',
                'borderWidth': 1
            }
        ]
    }
    
    return JsonResponse(data)


def performance_chart_data(request):
    """API endpoint for performance rating distribution chart"""
    # Get performance rating distribution
    rating_distribution = Performance.objects.values('rating').annotate(
        count=Count('id')
    ).order_by('rating')
    
    rating_labels = {
        1: 'Poor',
        2: 'Below Average',
        3: 'Average',
        4: 'Good',
        5: 'Excellent'
    }
    
    labels = []
    data = []
    colors = ['#FF6384', '#FF9F40', '#FFCE56', '#4BC0C0', '#36A2EB']
    
    for rating_data in rating_distribution:
        rating = rating_data['rating']
        labels.append(rating_labels.get(rating, f'Rating {rating}'))
        data.append(rating_data['count'])
    
    chart_data = {
        'labels': labels,
        'data': data,
        'backgroundColor': colors[:len(labels)]
    }
    
    return JsonResponse(chart_data)


def dashboard_stats(request):
    """API endpoint for dashboard statistics"""
    # Overall statistics
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(is_active=True).count()
    total_departments = Department.objects.count()
    
    # Today's attendance
    today = timezone.now().date()
    today_attendance = Attendance.objects.filter(date=today)
    present_today = today_attendance.filter(status='present').count()
    absent_today = today_attendance.filter(status='absent').count()
    late_today = today_attendance.filter(status='late').count()
    
    # Performance statistics
    avg_performance = Performance.objects.aggregate(
        avg_rating=Avg('rating')
    )['avg_rating'] or 0
    
    # Recent activities
    recent_employees = Employee.objects.order_by('-created_at')[:5]
    recent_attendances = Attendance.objects.select_related('employee').order_by('-date')[:5]
    recent_performances = Performance.objects.select_related('employee').order_by('-review_date')[:5]
    
    stats = {
        'overall': {
            'total_employees': total_employees,
            'active_employees': active_employees,
            'total_departments': total_departments,
            'avg_performance': round(avg_performance, 2)
        },
        'today_attendance': {
            'present': present_today,
            'absent': absent_today,
            'late': late_today,
            'total': today_attendance.count()
        },
        'recent_activities': {
            'employees': [
                {
                    'name': emp.name,
                    'department': emp.department.name,
                    'created_at': emp.created_at.strftime('%Y-%m-%d')
                } for emp in recent_employees
            ],
            'attendances': [
                {
                    'employee': att.employee.name,
                    'status': att.status,
                    'date': att.date.strftime('%Y-%m-%d')
                } for att in recent_attendances
            ],
            'performances': [
                {
                    'employee': perf.employee.name,
                    'rating': perf.rating,
                    'review_date': perf.review_date.strftime('%Y-%m-%d')
                } for perf in recent_performances
            ]
        }
    }
    
    return JsonResponse(stats)
