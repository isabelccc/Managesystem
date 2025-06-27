from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from employees.models import Department, Employee
from attendance.models import Attendance
from performance.models import Performance
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed the database with fake employee data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--employees',
            type=int,
            default=50,
            help='Number of employees to create (default: 50)'
        )

    def handle(self, *args, **options):
        num_employees = options['employees']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting to seed database with {num_employees} employees...')
        )

        with transaction.atomic():
            # Create departments
            departments = self.create_departments()
            
            # Create employees
            employees = self.create_employees(departments, num_employees)
            
            # Create attendance records
            self.create_attendance_records(employees)
            
            # Create performance records
            self.create_performance_records(employees)

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database!')
        )

    def create_departments(self):
        """Create sample departments"""
        departments_data = [
            {'name': 'Engineering', 'description': 'Software development and technical operations'},
            {'name': 'Marketing', 'description': 'Marketing and communications'},
            {'name': 'Sales', 'description': 'Sales and business development'},
            {'name': 'Human Resources', 'description': 'HR and recruitment'},
            {'name': 'Finance', 'description': 'Finance and accounting'},
            {'name': 'Operations', 'description': 'Operations and logistics'},
            {'name': 'Customer Support', 'description': 'Customer service and support'},
            {'name': 'Product Management', 'description': 'Product strategy and management'},
        ]
        
        departments = []
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults=dept_data
            )
            departments.append(dept)
            if created:
                self.stdout.write(f'Created department: {dept.name}')
        
        return departments

    def create_employees(self, departments, num_employees):
        """Create sample employees"""
        first_names = [
            'John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa',
            'James', 'Jennifer', 'William', 'Jessica', 'Richard', 'Amanda', 'Thomas',
            'Nicole', 'Christopher', 'Stephanie', 'Daniel', 'Melissa', 'Matthew',
            'Ashley', 'Anthony', 'Elizabeth', 'Mark', 'Megan', 'Donald', 'Lauren',
            'Steven', 'Rachel', 'Paul', 'Kimberly', 'Andrew', 'Heather', 'Joshua',
            'Michelle', 'Kenneth', 'Tiffany', 'Kevin', 'Christina', 'Brian', 'Laura',
            'George', 'Amber', 'Edward', 'Danielle', 'Ronald', 'Brittany', 'Timothy',
            'Rebecca', 'Jason', 'Samantha'
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
            'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
            'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
            'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark',
            'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King',
            'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green',
            'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
            'Carter', 'Roberts'
        ]
        
        employees = []
        for i in range(num_employees):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            name = f"{first_name} {last_name}"
            email = f"{first_name.lower()}.{last_name.lower()}@company.com"
            phone = f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            
            # Random address
            addresses = [
                f"{random.randint(100, 9999)} Main St, City, State {random.randint(10000, 99999)}",
                f"{random.randint(100, 9999)} Oak Ave, Town, State {random.randint(10000, 99999)}",
                f"{random.randint(100, 9999)} Pine Rd, Village, State {random.randint(10000, 99999)}",
            ]
            address = random.choice(addresses)
            
            # Random joining date (within last 5 years)
            days_ago = random.randint(0, 1825)  # 5 years
            date_of_joining = date.today() - timedelta(days=days_ago)
            
            department = random.choice(departments)
            gender = random.choice(['M', 'F', 'O'])
            salary = random.randint(30000, 150000)
            
            employee = Employee.objects.create(
                name=name,
                email=email,
                phone_number=phone,
                address=address,
                date_of_joining=date_of_joining,
                department=department,
                gender=gender,
                salary=salary,
                is_active=random.choice([True, True, True, False])  # 75% active
            )
            employees.append(employee)
            
            if i % 10 == 0:
                self.stdout.write(f'Created employee {i+1}/{num_employees}: {name}')
        
        return employees

    def create_attendance_records(self, employees):
        """Create attendance records for the last 30 days"""
        self.stdout.write('Creating attendance records...')
        
        for employee in employees:
            # Create attendance for the last 30 days
            for i in range(30):
                attendance_date = date.today() - timedelta(days=i)
                
                # Skip weekends (Saturday=5, Sunday=6)
                if attendance_date.weekday() >= 5:
                    continue
                
                # Random attendance status
                status_weights = {'present': 0.7, 'absent': 0.1, 'late': 0.15, 'half_day': 0.05}
                status = random.choices(
                    list(status_weights.keys()),
                    weights=list(status_weights.values())
                )[0]
                
                # Random check-in and check-out times
                check_in_hour = random.randint(7, 10) if status != 'absent' else None
                check_in_minute = random.randint(0, 59) if check_in_hour else None
                check_out_hour = random.randint(16, 19) if status in ['present', 'late'] else None
                check_out_minute = random.randint(0, 59) if check_out_hour else None
                
                from datetime import time
                check_in_time = time(check_in_hour, check_in_minute) if check_in_hour else None
                check_out_time = time(check_out_hour, check_out_minute) if check_out_hour else None
                
                Attendance.objects.create(
                    employee=employee,
                    date=attendance_date,
                    status=status,
                    check_in_time=check_in_time,
                    check_out_time=check_out_time,
                    notes=random.choice(['', 'Good day', 'Busy day', 'Team meeting']) if status != 'absent' else 'Called in sick'
                )

    def create_performance_records(self, employees):
        """Create performance records for employees"""
        self.stdout.write('Creating performance records...')
        
        reviewers = ['John Manager', 'Sarah Director', 'Mike Supervisor', 'Lisa HR', 'David Lead']
        
        for employee in employees:
            # Create 1-3 performance reviews per employee
            num_reviews = random.randint(1, 3)
            
            for i in range(num_reviews):
                # Review date within last 2 years
                days_ago = random.randint(0, 730)
                review_date = date.today() - timedelta(days=days_ago)
                
                # Random rating (weighted towards better ratings)
                rating_weights = {1: 0.05, 2: 0.1, 3: 0.3, 4: 0.4, 5: 0.15}
                rating = random.choices(
                    list(rating_weights.keys()),
                    weights=list(rating_weights.values())
                )[0]
                
                # Next review date (6-12 months from review date)
                months_ahead = random.randint(6, 12)
                next_review_date = review_date + timedelta(days=months_ahead * 30)
                
                comments = [
                    'Good performance overall',
                    'Shows great potential',
                    'Needs improvement in some areas',
                    'Excellent work ethic',
                    'Consistent performer',
                    'Team player',
                    'Strong technical skills',
                    'Good communication skills'
                ]
                
                goals = [
                    'Improve technical skills',
                    'Take on more leadership responsibilities',
                    'Enhance communication skills',
                    'Complete advanced training',
                    'Mentor junior team members'
                ]
                
                achievements = [
                    'Completed major project on time',
                    'Received positive feedback from clients',
                    'Improved team productivity',
                    'Successfully led a team',
                    'Implemented new process improvements'
                ]
                
                areas_for_improvement = [
                    'Time management',
                    'Technical skills',
                    'Communication',
                    'Leadership',
                    'Problem solving'
                ]
                
                Performance.objects.create(
                    employee=employee,
                    rating=rating,
                    review_date=review_date,
                    reviewer=random.choice(reviewers),
                    comments=random.choice(comments),
                    goals=random.choice(goals),
                    achievements=random.choice(achievements),
                    areas_for_improvement=random.choice(areas_for_improvement),
                    next_review_date=next_review_date
                ) 