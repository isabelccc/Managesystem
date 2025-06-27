from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Attendance
from .serializers import AttendanceSerializer, AttendanceDetailSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    """ViewSet for Attendance model with CRUD operations"""
    queryset = Attendance.objects.select_related('employee', 'employee__department').all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'status', 'date']
    search_fields = ['employee__name', 'employee__department__name']
    ordering_fields = ['date', 'employee__name', 'status']
    ordering = ['-date', 'employee__name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AttendanceDetailSerializer
        return AttendanceSerializer

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's attendance records"""
        today = timezone.now().date()
        attendances = self.queryset.filter(date=today)
        serializer = self.get_serializer(attendances, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get attendance statistics"""
        # Get date range from query params
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            # Default to current month
            today = timezone.now().date()
            start_date = today.replace(day=1)
            end_date = today

        # Filter attendances by date range
        attendances = self.queryset.filter(date__range=[start_date, end_date])
        
        # Calculate statistics
        total_records = attendances.count()
        present_count = attendances.filter(status='present').count()
        absent_count = attendances.filter(status='absent').count()
        late_count = attendances.filter(status='late').count()
        
        # Calculate attendance rate
        attendance_rate = (present_count / total_records * 100) if total_records > 0 else 0
        
        # Department-wise statistics
        dept_stats = attendances.values('employee__department__name').annotate(
            total=Count('id'),
            present=Count('id', filter=Q(status='present')),
            absent=Count('id', filter=Q(status='absent')),
            late=Count('id', filter=Q(status='late'))
        )
        
        return Response({
            'date_range': {
                'start_date': start_date,
                'end_date': end_date
            },
            'overall_stats': {
                'total_records': total_records,
                'present': present_count,
                'absent': absent_count,
                'late': late_count,
                'attendance_rate': round(attendance_rate, 2)
            },
            'department_stats': dept_stats
        })

    @action(detail=False, methods=['get'])
    def monthly_overview(self, request):
        """Get monthly attendance overview for charts"""
        year = request.query_params.get('year', timezone.now().year)
        month = request.query_params.get('month', timezone.now().month)
        
        # Get all dates in the month
        start_date = datetime(int(year), int(month), 1).date()
        if int(month) == 12:
            end_date = datetime(int(year) + 1, 1, 1).date() - timedelta(days=1)
        else:
            end_date = datetime(int(year), int(month) + 1, 1).date() - timedelta(days=1)
        
        # Get daily attendance counts
        daily_stats = []
        current_date = start_date
        while current_date <= end_date:
            day_attendances = self.queryset.filter(date=current_date)
            daily_stats.append({
                'date': current_date,
                'present': day_attendances.filter(status='present').count(),
                'absent': day_attendances.filter(status='absent').count(),
                'late': day_attendances.filter(status='late').count(),
                'total': day_attendances.count()
            })
            current_date += timedelta(days=1)
        
        return Response({
            'year': year,
            'month': month,
            'daily_stats': daily_stats
        })
