from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Performance
from .serializers import PerformanceSerializer, PerformanceDetailSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    """ViewSet for Performance model with CRUD operations"""
    queryset = Performance.objects.select_related('employee', 'employee__department').all()
    serializer_class = PerformanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'rating', 'review_date']
    search_fields = ['employee__name', 'employee__department__name', 'reviewer']
    ordering_fields = ['review_date', 'rating', 'employee__name']
    ordering = ['-review_date', 'employee__name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PerformanceDetailSerializer
        return PerformanceSerializer

    @action(detail=False, methods=['get'])
    def overdue_reviews(self, request):
        """Get overdue performance reviews"""
        overdue_reviews = self.queryset.filter(
            next_review_date__lt=timezone.now().date()
        )
        serializer = self.get_serializer(overdue_reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming_reviews(self, request):
        """Get upcoming performance reviews (next 30 days)"""
        thirty_days_from_now = timezone.now().date() + timedelta(days=30)
        upcoming_reviews = self.queryset.filter(
            next_review_date__lte=thirty_days_from_now,
            next_review_date__gte=timezone.now().date()
        )
        serializer = self.get_serializer(upcoming_reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get performance statistics"""
        # Get date range from query params
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            # Default to current year
            today = timezone.now().date()
            start_date = today.replace(month=1, day=1)
            end_date = today

        # Filter performances by date range
        performances = self.queryset.filter(review_date__range=[start_date, end_date])
        
        # Calculate overall statistics
        total_reviews = performances.count()
        avg_rating = performances.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        
        # Rating distribution
        rating_distribution = performances.values('rating').annotate(
            count=Count('id')
        ).order_by('rating')
        
        # Department-wise statistics
        dept_stats = performances.values('employee__department__name').annotate(
            total_reviews=Count('id'),
            avg_rating=Avg('rating')
        )
        
        # Top performers (rating >= 4)
        top_performers = performances.filter(rating__gte=4).select_related('employee')
        top_performers_data = PerformanceSerializer(top_performers, many=True).data
        
        return Response({
            'date_range': {
                'start_date': start_date,
                'end_date': end_date
            },
            'overall_stats': {
                'total_reviews': total_reviews,
                'average_rating': round(avg_rating, 2),
                'top_performers_count': top_performers.count()
            },
            'rating_distribution': rating_distribution,
            'department_stats': dept_stats,
            'top_performers': top_performers_data
        })

    @action(detail=False, methods=['get'])
    def rating_analysis(self, request):
        """Get detailed rating analysis for charts"""
        year = request.query_params.get('year', timezone.now().year)
        
        # Get performances for the specified year
        performances = self.queryset.filter(
            review_date__year=year
        )
        
        # Monthly rating averages
        monthly_stats = []
        for month in range(1, 13):
            month_performances = performances.filter(review_date__month=month)
            avg_rating = month_performances.aggregate(
                avg_rating=Avg('rating')
            )['avg_rating'] or 0
            monthly_stats.append({
                'month': month,
                'average_rating': round(avg_rating, 2),
                'total_reviews': month_performances.count()
            })
        
        # Department-wise average ratings
        dept_ratings = performances.values('employee__department__name').annotate(
            avg_rating=Avg('rating'),
            total_reviews=Count('id')
        )
        
        return Response({
            'year': year,
            'monthly_stats': monthly_stats,
            'department_ratings': dept_ratings
        })
