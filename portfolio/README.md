# Portfolio Application - Django User Profile System

A comprehensive Django-based portfolio application with extended user profiles, geographic location tracking, interactive maps, role-based access control, and activity logging. **Containerized with Docker for hassle-free setup.**

## 📋 Table of Contents

- [Overview](#overview)
- [Why Docker?](#why-docker)
- [Quick Start with Docker](#quick-start-with-docker) ⭐ **Recommended**
- [Features](#features)
- [Project Structure](#project-structure)
- [User Roles & Permissions](#user-roles--permissions)
- [Core Features Guide](#core-features-guide)
- [API Documentation](#api-documentation)
- [Admin Interface](#admin-interface)
- [Activity Logging](#activity-logging)
- [Development](#development)
- [Advanced Setup (Local Installation)](#advanced-setup-local-installation)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This Django application provides user profile management with geographic capabilities. It is designed to demonstrate modern web development practices including:

- Extended user profiles with custom fields
- Geographic location tracking using GeoDjango
- Interactive maps with Leaflet.js
- RESTful API with Django REST Framework
- Role-based access control
- Comprehensive activity logging
- Modern, responsive UI
- **Docker-based deployment for consistency across platforms**

### Technology Stack

- **Backend**: Django 5.2.8
- **Database**: SQLite with SpatiaLite (dev) / PostgreSQL with PostGIS (prod)
- **API**: Django REST Framework 3.16.1
- **Maps**: Leaflet.js + OpenStreetMap
- **Geospatial**: GeoDjango + GDAL 3.6.2
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Containerization**: Docker + Docker Compose (recommended)
- **Web Server**: Gunicorn (production)

---

## 🐳 Why Docker?

### The Challenge with Local Setup

This application uses **GeoDjango**, which requires **GDAL** (Geospatial Data Abstraction Library). Installing GDAL locally can be challenging because:

❌ **Complex Dependencies**
- Requires C++ build tools (Visual Studio on Windows, gcc/g++ on Linux)
- Multiple system libraries (GDAL, GEOS, PROJ)
- Version compatibility issues between Python and GDAL
- Different installation methods per operating system

❌ **Platform-Specific Issues**
- Windows: OSGeo4W or conda required, DLL naming conflicts
- Linux: Multiple package managers, library paths
- macOS: Homebrew dependencies, linking issues

❌ **Time-Consuming Setup**
- Can take 30-60 minutes to resolve all dependencies (trust me I've tried)
- Debugging cryptic error messages
- Environment conflicts with other projects

### The Docker Solution

✅ **Zero Local Dependencies**
- No need to install GDAL, C++ compilers, or system libraries
- Everything is pre-configured in the Docker image
- Works identically on Windows, Mac, and Linux

✅ **5-Minute Setup**
- `docker-compose up --build` - that's it!
- No environment variables to configure
- No PATH issues or library conflicts

✅ **Consistent Environment**
- Same versions across all machines
- Development matches production
- Easy team collaboration

✅ **Isolated & Clean**
- Doesn't affect your system Python
- No version conflicts with other projects
- Easy to remove completely

**Bottom Line**: Docker eliminates hours of troubleshooting and lets you focus on the application, not the infrastructure.

---

## 🚀 Quick Start with Docker

### Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- Download: https://www.docker.com/products/docker-desktop

### Step 1: Verify Docker Installation

```bash
# Check Docker is installed
docker --version

# Check Docker Compose is installed
docker-compose --version

# Ensure Docker is running (Docker Desktop should be started)
docker info
```

### Step 2: Build and Start the Application

```bash
# Navigate to the portfolio directory
cd portfolio

# Build and start the container
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d
```

**What happens during build:**
- Downloads Python 3.11 slim base image
- Installs GDAL and all geospatial libraries
- Installs C++ build tools automatically
- Installs Django and dependencies
- Runs database migrations
- Starts development server on port 8000

**Build time:** 5-10 minutes (first time only, then cached)

### Step 3: Create Superuser Account

In a new terminal:

```bash
# Create admin account
docker-compose exec web python manage.py createsuperuser

# Follow prompts:
# - Username: (choose username)
# - Email: (your email)
# - Password: (secure password)
```

### Step 4: Access the Application

| URL | Description |
|-----|-------------|
| http://localhost:8000/ | Home / Your Profile Page |
| http://localhost:8000/admin/ | Django Admin Interface |
| http://localhost:8000/api/ | REST API Root |
| http://localhost:8000/map/ | Interactive Map View |

**First login:**
1. YOu've got two options for login:
- Go to http://localhost:8000/admin/login/
OR
- Go to http://localhost:8000/signin/
2. Enter your superuser credentials
3. You'll be redirected to your profile page

### Step 5: Stop the Application

```bash
# Stop containers (Ctrl+C if running in foreground, or:)
docker-compose down

# Stop and remove all data (fresh start)
docker-compose down -v
```

---

## ⚡ Common Docker Commands that were useful during development and testing:

```bash
# View application logs
docker-compose logs -f web

# Restart after code changes
docker-compose restart web

# Run Django management commands
docker-compose exec web python manage.py <command>

# Access Django shell
docker-compose exec web python manage.py shell

# Run migrations
docker-compose exec web python manage.py migrate

# Create migrations
docker-compose exec web python manage.py makemigrations

# Collect static files
docker-compose exec web python manage.py collectstatic

# Access container bash
docker-compose exec web /bin/bash

# View running containers
docker ps

# Rebuild image from scratch
docker-compose build --no-cache
```

---

## ✨ Features

### 🔐 1. Extended User Profiles
- Personal information (name, email)
- Contact details (phone, address)
- Geographic location (latitude/longitude points)
- Automatic profile creation on user registration
- Profile edit interface with real-time validation

### 🗺️ 2. Interactive Maps
- Full-screen map view using Leaflet.js
- OpenStreetMap tiles for global coverage
- Custom gradient markers matching app theme
- Click markers to view user details in popups
- Auto-zoom to fit all markers perfectly
- Multiple access points (profile page, admin panel)
- GeoJSON API endpoint for location data

### 🔌 3. RESTful API
- Full CRUD operations on profiles
- User and profile endpoints with nested data
- GeoJSON format support for geographic data
- Session and token authentication
- Permission-based access control
- Browsable API interface

### 👥 4. Role-Based Access Control
- **Two User Levels**: Staff Users and Superusers (all registered users are staff)
- **Staff Users**: Can view/edit own profile only (via admin or web interface)
- **Superusers**: Full access to all profiles and admin features
- View-level permission enforcement
- API-level permission checks
- Group-based permissions using Django's Groups system

### 📊 5. Activity Logging
- Automatic login/logout tracking
- Failed login attempt monitoring for security
- IP address and user agent capture
- Beautiful admin interface with color-coding (Green/Gray/Red)
- Security monitoring and audit trail capabilities
- Data preserved even when users are deleted

### ⚙️ 6. Enhanced Admin Interface
- Custom GIS admin with interactive map widgets
- One-click "View on Map" buttons
- Enhanced user profile management
- Activity log viewing with advanced filters
- Search across multiple fields
- Custom actions and bulk operations

### 🎨 7. Modern UI
- Responsive gradient design (purple theme)
- Mobile-friendly layout with touch support
- Color-coded visual feedback
- Intuitive navigation with breadcrumbs
- Form validation with inline error messages
- Loading states and smooth transitions

### 🐳 8. Docker Support
- One-command deployment
- Pre-configured environment with all dependencies
- No local GDAL/C++ build tools required
- Consistent across all platforms
- Easy scaling and production deployment

---

## 🏗️ Production Deployment with PostgreSQL

For production environments, we recommend using PostgreSQL with PostGIS for better performance and scalability.

### Using docker-compose.prod.yml

The project includes a production-ready Docker Compose configuration:

```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up -d --build

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

### What's Included in Production Setup

- **Gunicorn** web server with 4 workers
- **Nginx** reverse proxy
- **Static file serving** via Nginx
- **Persistent volumes** for data and static files
- **Automatic restarts** if containers fail
- **Optimized settings** for production

### Environment Variables for Production

Create a `.env` file:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgis://user:password@db:5432/portfolio
```

---

## 📁 Project Structure

```
portfolio/
├── app/                              # Main Django application
│   ├── migrations/                   # Database migrations
│   ├── templates/                    # HTML templates
│   │   ├── admin/                    # Custom admin templates
│   │   │   └── app/
│   │   │       └── userprofile/
│   │   │           └── change_list.html
│   │   └── app/
│   │       ├── base.html             # Base template with navigation
│   │       ├── profile_view.html     # Profile display page
│   │       ├── profile_edit.html     # Profile editing page
│   │       └── map_view.html         # Interactive map view
│   ├── __init__.py
│   ├── admin.py                      # Admin interface configuration
│   ├── apps.py                       # App configuration
│   ├── forms.py                      # Django forms for profile editing
│   ├── models.py                     # Database models (UserProfile, ActivityLog)
│   ├── serializers.py                # DRF serializers for API
│   ├── signals.py                    # Signal handlers for activity logging
│   ├── tests.py                      # Test cases
│   └── views.py                      # View functions and API viewsets
├── portfolio/                        # Project configuration
│   ├── __init__.py
│   ├── asgi.py                       # ASGI configuration
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # URL routing
│   └── wsgi.py                       # WSGI configuration
├── manage.py                         # Django management script
├── db.sqlite3                        # SQLite database (local dev)
├── requirements.txt                  # Python dependencies (create if needed)
├── Dockerfile                        # Docker configuration (create if using Docker)
├── docker-compose.yml                # Docker Compose config (create if using Docker)
└── README.md                         # This file
```

---

## 👥 User Roles & Permissions

The application implements **two levels of user access**:

> **Note**: All users who register via `/signup/` are automatically created as **Staff Users**. There are no "regular users" - everyone has staff access by default.

### Staff User (Default for All Registered Users)
- ✅ View and edit **own profile only** (via web interface or admin)
- ✅ View own location on map
- ✅ Access Django admin interface
- ✅ Access REST API for **own data only**
- ✅ View own activity logs in admin
- ✅ Member of "Staff" group with UserProfile view/edit permissions
- ❌ **Cannot** view other users' profiles
- ❌ **Cannot** view all users on map
- ❌ **Cannot** access all data via API
- ❌ **Cannot** delete any records
- ❌ **Cannot** manage users, groups, or permissions

**Created by:** Signing up at `/signup/` or via Django shell

### Superuser ⭐ (Administrator)
- ✅ **Full access** to everything
- ✅ View and edit **any user's profile**
- ✅ Access **all Django admin models**
- ✅ View **all users on map**
- ✅ Access **all data via API**
- ✅ View and manage **all activity logs**
- ✅ Delete any records
- ✅ Manage users, groups, and permissions
- ✅ Bypass all permission restrictions

**Created by:** `python manage.py createsuperuser` command

### Permission Matrix

| Feature | Staff User | Superuser |
|---------|------------|-----------|
| **Web Interface** | | |
| View own profile | ✅ | ✅ |
| Edit own profile | ✅ | ✅ |
| View other profiles | ❌ | ✅ |
| **Admin Panel** | | |
| Access /admin/ | ✅ | ✅ |
| View own UserProfile | ✅ | ✅ |
| View all UserProfiles | ❌ | ✅ |
| Edit own UserProfile | ✅ | ✅ |
| Edit any UserProfile | ❌ | ✅ |
| Delete profiles | ❌ | ✅ |
| View own User account | ✅ | ✅ |
| View all Users | ❌ | ✅ |
| Manage groups/permissions | ❌ | ✅ |
| **Maps** | | |
| View own location | ✅ | ✅ |
| View all users on map | ❌ | ✅ |
| **Activity Logs** | | |
| View own logs | ✅ | ✅ |
| View all logs | ❌ | ✅ |
| Delete logs | ❌ | ✅ |
| **REST API** | | |
| Access own data | ✅ | ✅ |
| Access all data | ❌ | ✅ |

### Technical Implementation

**Staff Users** (`is_staff=True`, `is_superuser=False`):
- Automatically assigned to "Staff" Django Group on registration
- Group has `view_userprofile` and `change_userprofile` permissions
- Custom admin methods filter querysets to show only own data
- Cannot create accounts via admin (must use signup page)

**Superusers** (`is_superuser=True`):
- Created via `createsuperuser` command
- Automatically have all permissions
- Not in any groups (don't need them)
- Can create/edit/delete any records

---

## 📚 Core Features Guide

### 1. User Profiles

#### Viewing Your Profile

1. Log in at `/admin/login/`
2. Automatically redirected to `/profile/`
3. See your profile information organized in sections:
   - **Account Information** (role, date joined)
   - **Personal Information** (name, email)
   - **Contact Information** (phone, address)
   - **Geographic Location** (coordinates)

#### Editing Your Profile

1. Click "Edit Profile" button
2. Update fields:
   - First Name, Last Name, Email
   - Phone Number, Home Address
   - Latitude and Longitude for location
3. Click "Save Changes"

**Finding Your Coordinates:**
1. Open Google Maps
2. Right-click on your location
3. Click the coordinates to copy
4. First number = Latitude, Second number = Longitude

**Example Coordinates:**
- New York: `40.7128, -74.0060`
- London: `51.5074, -0.1278`
- Tokyo: `35.6762, 139.6503`

#### Viewing Other Profiles (Superuser Only)

1. Access `/profile/<username>/`
2. See "Viewing as Superuser" badge
3. Profile is read-only (no edit button)

### 2. Interactive Maps

#### Access Points

**From Profile Page:**
- "View on Map" button appears when location is set
- Opens map centered on your location

**From Admin (Superuser):**
- **List View**: Click "View on Map" button in user row
- **Toolbar**: Click "View All Users on Map"
- **Change Form**: Click "View This User on Map" link

#### Map Features

- **Full-screen** interactive map
- **Custom markers** with purple gradient
- **Click markers** to see user details in popup
- **Auto-zoom** to fit all markers
- **Pan and zoom** for navigation
- **Loading indicator** while data loads

#### Map URLs

| URL | What It Shows |
|-----|---------------|
| `/map/` | All users (superuser) or own location (staff user) |
| `/map/?user_id=1` | Specific user's location (superuser only) |

### 3. REST API

#### Endpoints

```
# API Root
GET    /api/

# Users (with nested profiles)
GET    /api/users/              # List all users
GET    /api/users/{id}/         # Get specific user

# User Profiles
GET    /api/profiles/           # List profiles
GET    /api/profiles/{id}/      # Get specific profile
PUT    /api/profiles/{id}/      # Full update
PATCH  /api/profiles/{id}/      # Partial update
POST   /api/profiles/           # Create (usually auto-created)
DELETE /api/profiles/{id}/      # Delete

# Map Data (GeoJSON)
GET    /map/api/locations/      # All locations in GeoJSON format
GET    /map/api/locations/?user_id=1  # Specific user location
```

#### Authentication

The API uses session authentication. Log in first:

```bash
# Login via browser
Open http://localhost:8000/api-auth/login/

# Then access API endpoints
```

#### Example API Calls

**Get Your Profile:**
```bash
curl -b cookies.txt http://localhost:8000/api/profiles/
```

**Update Profile:**
```bash
curl -X PATCH http://localhost:8000/api/profiles/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "home_address": "123 Main St, New York, NY 10001",
    "phone_number": "+1-555-123-4567",
    "location": {
      "type": "Point",
      "coordinates": [-74.0060, 40.7128]
    }
  }'
```

#### Response Formats

**Profile Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "home_address": "123 Main St, NYC",
  "phone_number": "+1-555-123-4567",
  "location": {
    "type": "Point",
    "coordinates": [-74.0060, 40.7128]
  },
  "created_at": "2025-11-11T10:00:00Z",
  "updated_at": "2025-11-11T12:00:00Z"
}
```

**GeoJSON Response:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-74.0060, 40.7128]
      },
      "properties": {
        "username": "john_doe",
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone_number": "+1-555-123-4567",
        "home_address": "123 Main St",
        "user_id": 1
      }
    }
  ]
}
```

### 4. Admin Interface

#### Accessing Admin

1. Navigate to `/admin/`
2. Login with staff or superuser credentials
3. See available models based on permissions

#### User Profiles Admin

**Features:**
- List view with search and filters
- GIS map widget for location selection
- "View on Map" buttons
- Search by username, email, phone, address
- Filter by creation/update dates
- Organized fieldsets in change form

**Map Integration:**
- Individual "View on Map" buttons per user
- "View All Users on Map" in toolbar
- "View This User on Map" link in change form

#### User Activity Logs Admin

**Features:**
- Color-coded display:
  - ✅ Green: Successful logins
  - 🚪 Gray: Logouts
  - ❌ Red: Failed login attempts
- Filters: Action, Date, User
- Search: Username, IP address, Email
- Date hierarchy: Year → Month → Day
- Read-only (automatically generated)
- Only superusers can delete

**Information Displayed:**
- Action type with icon
- Username (preserved even if user deleted)
- Link to user account (if exists)
- Timestamp
- IP address
- Browser/Device info (shortened)
- Session key (in detail view)

### 5. Activity Logging

#### What Gets Logged

Every authentication event is automatically logged:

- ✅ **Successful Logins**: When user logs in
- 🚪 **Logouts**: When user logs out
- ❌ **Failed Attempts**: When login fails (wrong password)

#### Information Captured

For each event:
- Username (never lost, even if user deleted)
- User account link (if user still exists)
- Action type (login/logout/failed_login)
- Precise timestamp
- IP address (client's IP)
- User agent (browser and device info)
- Session key (for correlation)

#### Viewing Activity Logs

1. Log in as superuser
2. Navigate to Admin → User Activity Logs
3. See all events in reverse chronological order

#### Filtering and Search

**Quick Filters:**
- Action: Show only logins, logouts, or failed attempts
- Date: Today, Past 7 days, This month, etc.
- User: Select specific user

**Search:**
- By username
- By IP address
- By email

**Date Navigation:**
- Click year → month → day in hierarchy
- Browse events for specific dates

#### Security Monitoring

**Use Cases:**
- Detect brute force attacks (multiple failed attempts)
- Monitor suspicious IP addresses
- Track user access patterns
- Investigate security incidents
- Audit trail for compliance

**Example Queries (Django Shell):**
```python
from app.models import UserActivityLog
from django.utils import timezone
from datetime import timedelta

# Failed logins in last 24 hours
recent_failures = UserActivityLog.objects.filter(
    action='failed_login',
    timestamp__gte=timezone.now() - timedelta(days=1)
)

# Specific user's login history
user_history = UserActivityLog.objects.filter(
    username='john_doe',
    action='login'
).order_by('-timestamp')

# All activity from an IP address
ip_activity = UserActivityLog.objects.filter(
    ip_address='192.168.1.100'
)
```

---

## 🔍 Troubleshooting

### Docker-Related Issues

#### Container Won't Start

**Problem:** Container exits immediately or fails to build

**Check logs:**
```bash
docker-compose logs web
```

**Common solutions:**
```bash
# Rebuild without cache
docker-compose build --no-cache

# Check Docker Desktop is running
docker info

# Remove and recreate containers
docker-compose down -v
docker-compose up --build
```

#### Port 8000 Already in Use

**Error:** `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution:** Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use port 8001 instead
```

Then access at `http://localhost:8001/`

#### Database Locked Error (SQLite)

**Problem:** `database is locked` error in Docker

**Solution:** Restart the container:
```bash
docker-compose restart web
```

For production, use PostgreSQL (see Production Deployment section)

#### Changes Not Reflecting

**Problem:** Code changes don't appear in running container

**Solution:**
```bash
# Restart the container
docker-compose restart web

# If still not working, rebuild
docker-compose up --build
```

### Application Issues

#### Permission Denied / Can't Access Admin or Other Profiles

**Problem:** Staff users can't access admin or other profiles

**Expected behavior:**
- All registered users have `is_staff=True` (admin access)
- Staff users can only see their **own** profile (not others)
- Viewing **all** profiles requires `is_superuser=True`

**Check user permissions:**
```bash
docker-compose exec web python manage.py shell
```
```python
from django.contrib.auth.models import User, Group

user = User.objects.get(username='your_username')
print(f"Staff: {user.is_staff}, Superuser: {user.is_superuser}")
print(f"Groups: {[g.name for g in user.groups.all()]}")

# All registered users should have:
# - is_staff=True
# - is_superuser=False (unless created as superuser)
# - Be in the "Staff" group
```

#### Map Not Loading

**Problem:** Blank map or stuck on loading screen

**Solutions:**
1. Check browser console (F12) for errors
2. Ensure user has location set (latitude/longitude)
3. Verify internet connection (map tiles load from CDN)
4. Check Docker logs for API errors

#### Activity Logs Not Appearing

**Problem:** No logs created when logging in/out

**Solution:** Ensure migrations have run:
```bash
docker-compose exec web python manage.py migrate
docker-compose restart web
```

#### "View All Users on Map" Error

**Problem:** Error when clicking "View All Users on Map" in admin

**This has been fixed!** The issue was with `user_id=None` being passed as a string. If you encounter this:
```bash
# Pull latest code and restart
git pull
docker-compose restart web
```

### Getting More Help

**View detailed logs:**
```bash
# All logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f web

# Last 100 lines
docker-compose logs --tail=100 web
```

**Access container shell for debugging:**
```bash
docker-compose exec web /bin/bash

# Inside container, you can:
python manage.py shell
python manage.py check
python manage.py showmigrations
```

**Check database:**
```bash
docker-compose exec web python manage.py dbshell
```

---

## 🛠️ Advanced Setup (Local Installation)

> ⚠️ **Warning**: Local installation requires complex dependencies including C++ build tools and GDAL. **We strongly recommend using Docker instead** (see Quick Start section above).

### Why Local Setup is Complex

Installing this application locally requires:
- C++ compiler (Visual Studio Build Tools on Windows, gcc/g++ on Linux)
- GDAL library with matching Python bindings
- Multiple system libraries (GEOS, PROJ, SpatiaLite)
- Platform-specific configuration
- Potential conflicts with other Python projects

**Estimated setup time:** 30-60 minutes (vs. 5 minutes with Docker)

### Prerequisites for Local Installation

- Python 3.11
- C++ Build Tools:
  - **Windows**: Visual Studio Build Tools or MinGW
  - **Linux**: `build-essential` package
  - **macOS**: Xcode Command Line Tools
- GDAL 3.6+ with development headers

### Step 1: Install System Dependencies

**Windows (using conda - Recommended):**
```bash
# Install Miniconda first: https://docs.conda.io/en/latest/miniconda.html
conda create -n portfolio python=3.11 "gdal=3.10.3" -c conda-forge
conda activate portfolio

# Fix DLL naming issue (Windows only)
copy "%CONDA_PREFIX%\Library\bin\gdal.dll" "%CONDA_PREFIX%\Library\bin\gdal310.dll"

# Install Django packages
pip install django djangorestframework gunicorn
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y \
    python3.11 \
    python3.11-venv \
    gdal-bin \
    libgdal-dev \
    g++ \
    gcc \
    build-essential \
    libsqlite3-mod-spatialite
```

**macOS:**
```bash
brew install python@3.11 gdal
```

### Step 2: Setup Python Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Python packages
pip install django djangorestframework gunicorn

# Install GDAL Python bindings (match system version)
pip install GDAL==$(gdal-config --version)
```

### Step 3: Configure and Run

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Local Installation Troubleshooting

#### GDAL Not Found

**Error:** `Could not find the GDAL library`

**Windows:** Ensure `gdal310.dll` exists (see Step 1)
**Linux:** `export GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgdal.so`
**Mac:** `export GDAL_LIBRARY_PATH=/opt/homebrew/lib/libgdal.dylib`

#### C++ Compiler Missing

**Error:** `error: Microsoft Visual C++ 14.0 or greater is required`

**Solution:** Install Visual Studio Build Tools:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

#### Version Conflicts

**Error:** `GDAL version mismatch`

**Solution:** Match Python GDAL version to system:
```bash
# Check system version
gdal-config --version

# Install matching Python package
pip install GDAL==<version>
```

### Why We Recommend Docker

After setting up locally, you might encounter:
- DLL/library path issues
- Version mismatches
- Environment conflicts
- Platform-specific bugs
- Time spent debugging instead of developing

**Docker eliminates all of these issues.** Consider switching to Docker for a better experience.

---

## 🛠️ Development

### Running Tests

```bash
# Run all tests
python manage.py test app

# Run with verbosity
python manage.py test app -v 2

# Run specific test class
python manage.py test app.tests.UserProfileTestCase

# Run specific test method
python manage.py test app.tests.UserProfileTestCase.test_profile_created_automatically
```

### Creating New Users

**Via Signup Page (Recommended for Staff Users):**
1. Go to: http://localhost:8000/signup/
2. Fill in username, email, password
3. Automatically created with `is_staff=True`
4. Automatically added to "Staff" group
5. Profile automatically created via signal

**Via Admin Interface (Superuser Only):**
1. Login as superuser
2. Admin → Users → Add User
3. Set username and password
4. Save and continue editing
5. Set email, name, permissions, and staff/superuser flags
6. Profile automatically created via signal

**Via Command Line (For Superusers):**
```bash
# In Docker:
docker-compose exec web python manage.py createsuperuser

# Or locally:
python manage.py createsuperuser
```

**Via Django Shell:**
```python
from django.contrib.auth.models import User, Group

# Staff user (same as signup page creates)
staff = User.objects.create_user('staffuser', 'staff@example.com', 'password', is_staff=True)
staff_group = Group.objects.get(name='Staff')
staff.groups.add(staff_group)

# Superuser (administrator)
admin = User.objects.create_superuser('admin', 'admin@example.com', 'password')

# Note: All users registered via /signup/ are automatically staff users
# There are only two user levels: Staff and Superuser
```

### Database Management

**Backup Database:**
```bash
python manage.py dumpdata > backup.json
```

**Restore Database:**
```bash
python manage.py loaddata backup.json
```

**Reset Database:**
```bash
# Delete database file
rm db.sqlite3

# Run migrations
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

### Adding Profile Fields

1. **Update Model** (`app/models.py`):
```python
new_field = models.CharField(max_length=100, blank=True, null=True)
```

2. **Update Form** (`app/forms.py`):
```python
class UserProfileForm(forms.ModelForm):
    class Meta:
        fields = ['home_address', 'phone_number', 'new_field']
```

3. **Update Template** (`app/templates/app/profile_view.html`):
```html
<div class="info-item">
    <span class="info-label">New Field:</span>
    <span class="info-value">{{ profile.new_field }}</span>
</div>
```

4. **Create and Run Migration:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Customizing Theme

Edit `app/templates/app/base.html`:

```css
/* Change gradient colors */
body {
    background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
}

/* Change primary color */
.btn-primary {
    background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
}
```

### Production Deployment

**Settings to Change:**

1. **DEBUG**: Set to `False`
2. **SECRET_KEY**: Use environment variable
3. **ALLOWED_HOSTS**: Add your domain
4. **DATABASES**: Use PostgreSQL with PostGIS
5. **STATIC_ROOT**: Configure for static files
6. **Security Settings**:
   ```python
   CSRF_COOKIE_SECURE = True
   SESSION_COOKIE_SECURE = True
   SECURE_SSL_REDIRECT = True
   ```

**Collect Static Files:**
```bash
python manage.py collectstatic
```

---

## 📞 Support & Resources

### Getting Help

- Check this README for common issues
- Review `setup.txt` for implementation details
- Consult Django documentation: https://docs.djangoproject.com/
- GeoDjango tutorial: https://docs.djangoproject.com/en/4.2/ref/contrib/gis/tutorial/

### Project Documentation

- All features documented in this README
- Inline code comments in Python files
- Docstrings in functions and classes
- Type hints where applicable

### Key URLs (Running Locally)

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000/` | Home page / Your profile |
| `http://127.0.0.1:8000/admin/` | Django admin interface |
| `http://127.0.0.1:8000/profile/` | Your profile view |
| `http://127.0.0.1:8000/profile/edit/` | Edit your profile |
| `http://127.0.0.1:8000/map/` | Interactive map |
| `http://127.0.0.1:8000/api/` | REST API root |
| `http://127.0.0.1:8000/api/profiles/` | Profile API endpoint |
| `http://127.0.0.1:8000/api/users/` | Users API endpoint |

---

## 🎉 Quick Summary

### What This Project Does

A production-ready Django application demonstrating:

✅ **Extended User Profiles** - Beyond Django defaults with custom fields  
✅ **Geographic Location Tracking** - Point geometry with lat/lng coordinates  
✅ **Interactive Maps** - Full-screen Leaflet.js maps with custom markers  
✅ **RESTful API** - Complete CRUD operations with Django REST Framework  
✅ **Role-Based Access Control** - Two user levels (Staff and Superuser) with group-based permissions  
✅ **Activity Logging** - Automatic login/logout/failed attempt tracking  
✅ **Modern UI** - Responsive gradient design with mobile support  
✅ **Enhanced Admin** - GIS widgets, map integration, custom actions  
✅ **Security Features** - Permission checks, audit trails, CSRF protection  

### Why Use Docker for This Project?

🐳 **Docker Eliminates Setup Pain**
- ❌ No C++ build tools to install
- ❌ No GDAL library conflicts
- ❌ No platform-specific issues
- ✅ Works identically on Windows, Mac, Linux
- ✅ 5-minute setup vs 30-60 minutes locally
- ✅ Zero dependency conflicts

**Get started in 3 commands:**
```bash
cd portfolio
docker-compose up --build
docker-compose exec web python manage.py createsuperuser
```

### Key URLs

| URL | What It Does |
|-----|--------------|
| http://localhost:8000/ | Your profile page |
| http://localhost:8000/admin/ | Admin interface |
| http://localhost:8000/map/ | Interactive map |
| http://localhost:8000/api/ | REST API browser |

**Ready to go with Docker!** 🚀 See [Quick Start with Docker](#quick-start-with-docker) above.

---

## 📝 License

This project is for educational/portfolio purposes.

## 🙏 Acknowledgments

- **Django** and **Django REST Framework** teams for excellent web framework
- **GeoDjango** and **GDAL** communities for geospatial capabilities
- **Docker** for making deployment simple and consistent
- **Leaflet.js** for amazing mapping library
- **OpenStreetMap** contributors for free map tiles
- **Debian** project for solid container base images
