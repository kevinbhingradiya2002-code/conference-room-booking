# Conference Room Booking System

A Django web application for managing conference room reservations with user authentication, room management, and admin portal.

## Features

- **User Registration & Authentication**: Secure user accounts with profile management
- **Room Management**: Browse and search conference rooms with capacity and availability
- **Booking System**: Real-time room availability checking and conflict prevention
- **Reservation Management**: View, update, and cancel bookings
- **Admin Portal**: Manager dashboard for system administration
- **Notifications**: Real-time notifications for booking confirmations and updates
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Deployment**: Vercel
- **Version Control**: Git, GitHub

## Local Development Setup

### Prerequisites
- Python 3.11+
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
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

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate sample data**
   ```bash
   python manage.py populate_data
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open http://127.0.0.1:8000/ in your browser

## Test Accounts

- **Regular User**: `kevin` / `kevin123`
- **Manager**: `admin` / `admin123`

## Production Deployment

This application is configured for deployment on Vercel with PostgreSQL database.

### Environment Variables (Vercel)
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` for production
- `DATABASE_URL`: PostgreSQL connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## Project Structure

```
conference_room_booking/
├── bookings/                 # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms
│   ├── admin.py             # Admin interface
│   └── management/commands/  # Custom commands
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── conference_room_booking/  # Django project settings
├── requirements.txt         # Python dependencies
├── vercel.json             # Vercel deployment config
└── build_files.sh          # Build script for Vercel
```

## Management Commands

- `python manage.py populate_data`: Create sample rooms and users
- `python manage.py check_requirements`: Verify assignment requirements
- `python manage.py test_features`: Test core functionality
- `python manage.py test_booking`: Test booking system

## Assignment Requirements

This project fulfills all requirements for the conference room booking system assignment:

✅ Django as primary framework  
✅ SQLite database for development  
✅ Vercel deployment configuration  
✅ GitHub version control  
✅ User authentication and authorization  
✅ Room management and booking system  
✅ Admin portal for managers  
✅ Responsive design and notifications  

## License

This project is created for educational purposes as part of a university assignment.