# TicketLine - Conference Booking System

A Django web application for booking conference tickets with a multi-step checkout process.

## 🚀 Features

- **Conference Listing**: Browse available conferences
- **Multi-step Booking**: 4-step booking process (Select → Details → Payment → Success)
- **Admin Interface**: Manage conferences, tickets, attendees, and payments
- **Session Management**: Secure booking flow with session handling
- **Responsive Design**: Bootstrap-powered responsive UI

## 📋 Prerequisites

- Python 3.8+
- Django 5.2+
- Git (optional)

## 🛠️ Installation & Setup

### 1. Navigate to Project Directory

```bash
cd "/pathto/qn3/ticketline"
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv ticketline_env

# Activate virtual environment
# On macOS/Linux:
source ticketline_env/bin/activate

# On Windows:
# ticketline_env\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install Django (if not already installed)
pip install django

# Or if you have a requirements.txt file
pip install -r requirements.txt
```

### 4. Environment Configuration (Optional)

Create a `.env` file in the project root for environment-specific settings:

```bash
# Create .env file
touch .env
```

Add the following to your `.env` file:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
DJANGO_ADMIN_URL=secure-admin/

# Session Settings
SESSION_COOKIE_AGE=1800

# Database (for production)
# DATABASE_URL=postgres://username:password@localhost:5432/ticketline_db

# Email Settings (for production)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Database Setup

```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin Access)

```bash
python manage.py createsuperuser
```

Follow the prompts to create admin credentials.

### 7. Load Test Data (Optional)

```bash
# Load sample conferences and tickets
python manage.py load_test_data
```

This creates 3 sample conferences with tickets.

## 🚀 Running the Application

### Activate Virtual Environment (if using)

```bash
# On macOS/Linux:
source ticketline_env/bin/activate

# On Windows:
# ticketline_env\Scripts\activate
```

### Start Development Server

```bash
python manage.py runserver
```

The application will be available at:
- **Main Application**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/secure-admin/

## 📱 How to Use

### For Customers (Booking Process):

1. **Visit Homepage**: http://127.0.0.1:8000/
2. **Select Conference**: Choose from available conferences
3. **Enter Details**: Provide name and email
4. **Make Payment**: Select payment method and confirm
5. **Confirmation**: Receive booking confirmation with ticket number

### For Administrators:

1. **Access Admin**: http://127.0.0.1:8000/secure-admin/
2. **Login**: Use superuser credentials
3. **Manage Data**:
   - Add/edit conferences
   - Set ticket prices and availability
   - View bookings and payments
   - Manage attendees

## 📁 Project Structure

```
ticketline/
├── conferences/                 # Main app
│   ├── templates/conferences/   # HTML templates
│   │   ├── base.html
│   │   ├── conference_list.html
│   │   ├── attendee_details.html
│   │   ├── payment.html
│   │   └── success.html
│   ├── management/commands/     # Custom commands
│   │   └── load_test_data.py
│   ├── models.py               # Database models
│   ├── views.py                # Business logic
│   ├── admin.py                # Admin configuration
│   └── urls.py                 # App URLs
├── ticketline/                 # Project settings
│   ├── settings.py
│   └── urls.py
└── manage.py
```

## 🗄️ Database Models

- **Conference**: Event details (name, date, location)
- **Tickets**: Pricing and availability per conference
- **Attendee**: Customer information
- **CustomerTicket**: Booking records with unique ticket numbers
- **Payment**: Payment transaction records

## 🔧 Management Commands

### Load Test Data
```bash
python manage.py load_test_data
```
Creates sample conferences and tickets for testing.

### Standard Django Commands
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic
```

### Environment Management
```bash
# Create requirements.txt
pip freeze > requirements.txt

# Install from requirements.txt
pip install -r requirements.txt

# Deactivate virtual environment
deactivate
```

## 📦 Dependencies

Create a `requirements.txt` file with:

```txt
Django>=5.2.0
python-decouple>=3.6  # For .env file support (optional)
```

## 🌐 URLs

| URL | Description |
|-----|-------------|
| `/` | Conference listing page |
| `/book/<id>/` | Attendee details form |
| `/payment/<id>/` | Payment processing |
| `/success/` | Booking confirmation |
| `/secure-admin/` | Admin interface |

## 🔐 Admin Features

- **Conference Management**: Add/edit conferences
- **Ticket Management**: Set prices and availability
- **Booking Overview**: View all bookings and their status
- **Payment Tracking**: Monitor payment transactions (read-only)
- **Attendee Management**: View customer information

## 🛡️ Security Features

- **CSRF Protection**: All forms include CSRF tokens
- **Session Security**: Booking data stored securely in sessions
- **Admin URL**: Custom admin URL (`/secure-admin/`) for security
- **Input Validation**: Server-side form validation
- **Transaction Safety**: Database transactions for booking integrity

## 🚨 Troubleshooting

### Common Issues:

1. **Template Not Found**:
   ```bash
   # Ensure templates directory structure is correct
   conferences/templates/conferences/
   ```

2. **Database Errors**:
   ```bash
   # Reset database
   python manage.py migrate --run-syncdb
   ```

3. **Session Issues**:
   ```bash
   # Clear browser cookies or use incognito mode
   ```

4. **Static Files Not Loading**:
   ```bash
   # For development, ensure DEBUG=True in settings.py
   ```

## 📞 Support

For issues or questions:
1. Check the Django documentation: https://docs.djangoproject.com/
2. Review the code comments in views.py and models.py
3. Check the admin interface for data verification

## 🔄 Development Workflow

1. **Make Model Changes**: Edit `models.py`
2. **Create Migrations**: `python manage.py makemigrations`
3. **Apply Migrations**: `python manage.py migrate`
4. **Test Changes**: `python manage.py runserver`
5. **Update Admin**: Modify `admin.py` if needed

---

**Happy Booking! 🎫**
