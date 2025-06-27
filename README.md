# Employee Management System

A comprehensive Django-based Employee Management System with REST API, PostgreSQL database, and interactive dashboard with data visualization.

## Features

### Core Functionality
- **Employee Management**: CRUD operations for employees with department relationships
- **Department Management**: Organize employees by departments
- **Attendance Tracking**: Daily attendance records with status tracking
- **Performance Reviews**: Employee performance evaluation system
- **REST API**: Full CRUD APIs with filtering, searching, and pagination
- **Swagger Documentation**: Interactive API documentation
- **Data Visualization**: Interactive charts and dashboard
- **Authentication**: Token-based authentication
- **Database**: PostgreSQL with proper relationships and indexing

### Technical Features
- Django 5.2.3 with Django REST Framework
- PostgreSQL database with django-environ configuration
- Swagger/OpenAPI documentation with drf-yasg
- Interactive dashboard with Chart.js
- Docker and docker-compose support
- Management commands for data seeding
- Comprehensive admin interface

## Project Structure

```
Managesystem/
├── manage_system/          # Main Django project
├── employees/              # Employee and Department models
├── attendance/             # Attendance tracking
├── performance/            # Performance reviews
├── dashboard/              # Data visualization
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
└── README.md              # This file
```

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL
- Docker (optional)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Managesystem
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

5. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb manage_system_db
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Seed the database with sample data**
   ```bash
   python manage.py seed_data --employees 50
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations in container**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Seed data in container**
   ```bash
   docker-compose exec web python manage.py seed_data --employees 50
   ```

## API Endpoints

### Base URL
- Local: `http://localhost:8000/api/v1/`
- Docker: `http://localhost:8000/api/v1/`

### Authentication
The API uses Token Authentication. Include the token in the Authorization header:
```
Authorization: Token your-token-here
```

### Available Endpoints

#### Departments
- `GET /departments/` - List all departments
- `POST /departments/` - Create new department
- `GET /departments/{id}/` - Get department details
- `PUT /departments/{id}/` - Update department
- `DELETE /departments/{id}/` - Delete department
- `GET /departments/{id}/employees/` - Get employees in department
- `GET /departments/stats/` - Get department statistics

#### Employees
- `GET /employees/` - List all employees
- `POST /employees/` - Create new employee
- `GET /employees/{id}/` - Get employee details
- `PUT /employees/{id}/` - Update employee
- `DELETE /employees/{id}/` - Delete employee
- `GET /employees/{id}/attendance/` - Get employee attendance
- `GET /employees/{id}/performance/` - Get employee performance
- `GET /employees/stats/` - Get employee statistics

#### Attendance
- `GET /attendance/` - List all attendance records
- `POST /attendance/` - Create new attendance record
- `GET /attendance/{id}/` - Get attendance details
- `PUT /attendance/{id}/` - Update attendance
- `DELETE /attendance/{id}/` - Delete attendance
- `GET /attendance/today/` - Get today's attendance
- `GET /attendance/stats/` - Get attendance statistics
- `GET /attendance/monthly_overview/` - Get monthly overview

#### Performance
- `GET /performance/` - List all performance reviews
- `POST /performance/` - Create new performance review
- `GET /performance/{id}/` - Get performance details
- `PUT /performance/{id}/` - Update performance
- `DELETE /performance/{id}/` - Delete performance
- `GET /performance/overdue_reviews/` - Get overdue reviews
- `GET /performance/upcoming_reviews/` - Get upcoming reviews
- `GET /performance/stats/` - Get performance statistics
- `GET /performance/rating_analysis/` - Get rating analysis

### Query Parameters

#### Filtering
- `department` - Filter by department ID
- `status` - Filter attendance by status
- `date` - Filter by date
- `rating` - Filter performance by rating
- `is_active` - Filter employees by active status

#### Searching
- `search` - Search across name, email, phone fields

#### Ordering
- `ordering` - Order by any field (prefix with `-` for descending)

#### Pagination
- `page` - Page number
- `page_size` - Items per page (default: 20)

### Example API Calls

```bash
# Get all employees with pagination
curl -H "Authorization: Token your-token" \
     "http://localhost:8000/api/v1/employees/?page=1&page_size=10"

# Filter employees by department
curl -H "Authorization: Token your-token" \
     "http://localhost:8000/api/v1/employees/?department=1"

# Search employees
curl -H "Authorization: Token your-token" \
     "http://localhost:8000/api/v1/employees/?search=john"

# Get attendance statistics
curl -H "Authorization: Token your-token" \
     "http://localhost:8000/api/v1/attendance/stats/?start_date=2024-01-01&end_date=2024-01-31"
```

## Dashboard

Access the interactive dashboard at:
- Local: `http://localhost:8000/dashboard/`
- Docker: `http://localhost:8000/dashboard/`

### Dashboard Features
- **Statistics Cards**: Overview of key metrics
- **Department Chart**: Pie chart showing employee distribution
- **Performance Chart**: Doughnut chart showing rating distribution
- **Attendance Chart**: Bar chart showing monthly attendance overview

## Admin Interface

Access the Django admin at:
- Local: `http://localhost:8000/admin/`
- Docker: `http://localhost:8000/admin/`

## Swagger Documentation

Interactive API documentation available at:
- Local: `http://localhost:8000/swagger/`
- Docker: `http://localhost:8000/swagger/`

## Management Commands

### Seed Data
```bash
# Seed with default 50 employees
python manage.py seed_data

# Seed with custom number of employees
python manage.py seed_data --employees 100
```

## Database Models

### Department
- `name` - Department name (unique)
- `description` - Department description
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Employee
- `name` - Employee full name
- `email` - Email address (unique)
- `phone_number` - Phone number
- `address` - Address
- `date_of_joining` - Joining date
- `department` - Foreign key to Department
- `gender` - Gender choice
- `salary` - Salary amount
- `is_active` - Active status
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Attendance
- `employee` - Foreign key to Employee
- `date` - Attendance date
- `status` - Status (present/absent/late/half_day)
- `check_in_time` - Check-in time
- `check_out_time` - Check-out time
- `notes` - Additional notes
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Performance
- `employee` - Foreign key to Employee
- `rating` - Performance rating (1-5)
- `review_date` - Review date
- `reviewer` - Reviewer name
- `comments` - Review comments
- `goals` - Employee goals
- `achievements` - Employee achievements
- `areas_for_improvement` - Areas for improvement
- `next_review_date` - Next review date
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

## Environment Variables

Create a `.env` file with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://username:password@localhost:5432/manage_system_db
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.