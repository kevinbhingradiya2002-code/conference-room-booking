# Conference Room Booking System

A comprehensive web-based conference room reservation system built with Django for Te Whare Rūnanga Ltd.

## Features

### User Features
- **User Authentication**: Secure registration and login system
- **Room Browsing**: View available conference rooms with details
- **Room Search**: Filter rooms by capacity, date, and time availability
- **Reservation Management**: Create, view, edit, and cancel reservations
- **Notifications**: Receive confirmation and reminder notifications
- **Profile Management**: Update personal information and preferences

### Admin Features
- **Admin Dashboard**: Overview of system statistics and recent activity
- **Room Management**: Add, edit, and manage conference rooms
- **Reservation Management**: View and manage all reservations
- **User Management**: Manage user accounts and permissions
- **Notification System**: Send notifications to users

### Technical Features
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Real-time Availability**: Check room availability in real-time
- **Data Validation**: Comprehensive form validation and error handling
- **Security**: Built-in protection against common web vulnerabilities
- **Database Integration**: SQLite for development, PostgreSQL for production

## Technology Stack

As outlined in the Task 1 report, this project uses:

- **Backend**: Python with Django 4.2.7
- **Database**: SQLite (development) / PostgreSQL (production)
- **Data Access**: Django ORM
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Deployment**: Vercel

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd conference-room-booking
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create sample data**
   ```bash
   python manage.py populate_data
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

### Sample Accounts

After running `populate_data`, you can use these accounts:

- **Admin**: `admin` / `admin123`
- **Users**: `john.doe` / `password123`, `jane.smith` / `password123`, etc.

## Project Structure

```
conference_room_booking/
├── conference_room_booking/     # Django project settings
│   ├── settings.py             # Development settings
│   ├── settings_prod.py        # Production settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI configuration
├── bookings/                   # Main application
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── forms.py               # Django forms
│   ├── admin.py               # Admin configuration
│   ├── urls.py                # App URL patterns
│   └── management/            # Custom management commands
├── templates/                  # HTML templates
│   └── bookings/              # App-specific templates
├── static/                    # Static files (CSS, JS, images)
├── requirements.txt           # Development dependencies
├── requirements-prod.txt      # Production dependencies
├── vercel.json               # Vercel deployment configuration
└── manage.py                 # Django management script
```

## Database Models

### Room
- `name`: Room name (unique)
- `capacity`: Maximum number of people
- `location`: Physical location
- `description`: Room description
- `amenities`: Available amenities
- `is_active`: Availability status

### Reservation
- `room`: Foreign key to Room
- `user`: Foreign key to User
- `title`: Meeting title
- `description`: Meeting description
- `start_time`: Reservation start time
- `end_time`: Reservation end time
- `status`: Reservation status (pending, confirmed, cancelled, completed)
- `created_by_admin`: Whether created by admin

### UserProfile
- `user`: One-to-one relationship with User
- `phone_number`: Contact number
- `department`: User's department
- `is_admin`: Admin privileges

### Notification
- `user`: Foreign key to User
- `reservation`: Foreign key to Reservation
- `notification_type`: Type of notification
- `message`: Notification message
- `is_read`: Read status

## Key Features Implementation

### Security
- CSRF protection on all forms
- SQL injection protection via Django ORM
- XSS protection through template escaping
- User authentication and authorization

### User Experience
- Responsive design for all devices
- Intuitive navigation and user interface
- Real-time form validation
- Clear error messages and success notifications

### Admin Functionality
- Comprehensive admin dashboard
- Room management with CRUD operations
- Reservation management and oversight
- User account management
- System statistics and reporting

## Deployment

### Vercel Deployment

1. **Prepare for production**
   ```bash
   # Install production dependencies
   pip install -r requirements-prod.txt
   ```

2. **Configure environment variables**
   - `SECRET_KEY`: Django secret key
   - `POSTGRES_DATABASE`: Database name
   - `POSTGRES_USER`: Database user
   - `POSTGRES_PASSWORD`: Database password
   - `POSTGRES_HOST`: Database host
   - `POSTGRES_PORT`: Database port

3. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

### Testing
- Write unit tests for models and views
- Test form validation and error handling
- Test user authentication and authorization
- Test admin functionality

### Security Considerations
- Never commit sensitive information
- Use environment variables for secrets
- Regularly update dependencies
- Follow Django security best practices

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is developed for educational purposes as part of the ISCG7420 Web Application Development course.

## Contact

For questions or support, please contact the development team.

---

**Note**: This system is designed for Te Whare Rūnanga Ltd and follows the requirements specified in the assignment brief. The technology choices align with the Task 1 report recommendations, using Python with Django and Django ORM for optimal development efficiency and security.
