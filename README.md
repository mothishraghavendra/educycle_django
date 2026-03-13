# Educycle - Campus Exchange Platform

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-5.2.10-green)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/database-mysql-orange)](https://www.mysql.com/)
[![Status](https://img.shields.io/badge/status-active-brightgreen)]()

## Project Overview

**Educycle** is an enterprise-grade, open-source **student-to-student exchange platform** designed to facilitate secure peer-to-peer transactions within campus communities. The platform enables students to buy, sell, and donate items directly without intermediaries.

### Core Features

- **Buy & Sell** - Transparent pricing for pre-owned items
- **Free Donations** - Give away items to campus community
- **Direct Exchanges** - Secure peer-to-peer transactions
- **Campus-Centric** - In-person exchanges, no external logistics
- **User Verification** - Phone number and email validation
- **Transaction Tracking** - Complete exchange history and status management

---

## Table of Contents

- [Prerequisites](#-prerequisites)
- [System Requirements](#-system-requirements)
- [Project Architecture](#-project-architecture)
- [Tech Stack](#-tech-stack)
- [Installation & Setup](#-installation--setup)
- [Configuration](#-configuration)
- [File Structure](#-file-structure)
- [Features](#-features)
- [Security](#-security-features)
- [API Reference](#-api-reference-future-expansion)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Support](#-contact--support)

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.11+** - [Download](https://www.python.org/)
- **MySQL 8.0+** - [Download](https://www.mysql.com/)
- **Git** - [Download](https://git-scm.com/)
- **pip** - Python package manager (included with Python)

### Verify Installation
```bash
python --version          # Should show 3.11 or higher
mysql --version          # Should show 8.0 or higher
git --version            # Should show 2.0 or higher
pip --version            # Should show 21.0 or higher
```

---

## System Requirements

### Minimum Requirements
- **OS**: Linux, macOS, or Windows (with WSL2)
- **RAM**: 2GB
- **Disk Space**: 500MB
- **CPU**: 2 cores

### Recommended Requirements
- **OS**: Ubuntu 20.04 LTS or macOS 12+
- **RAM**: 4GB or more
- **Disk Space**: 2GB
- **CPU**: 4+ cores (for concurrent users)

---

## Project Architecture

## Project Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Educycle Platform Architecture                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────┐         ┌──────────────────┐                   │
│  │   Web Frontend   │────────▶│  Django Backend  │                   │
│  │                  │         │                  │                   │
│  │ • HTML5          │         │ • Views/URLs     │                   │
│  │ • CSS3           │         │ • ORM Models     │                   │
│  │ • JavaScript     │         │ • Business Logic │                   │
│  │ • Jinja2 Templ.  │         │ • Auth System    │                   │
│  │ • Static Files   │         │ • Middleware     │                   │
│  └──────────────────┘         └────────┬─────────┘                   │
│                                        │                              │
│                                        │                              │
│                            ┌───────────▼────────────┐                │
│                            │   MySQL Database       │                │
│                            │                        │                │
│                            │ • Users Table          │                │
│                            │ • Products Table       │                │
│                            │ • Exchanges Table      │                │
│                            │ • Auth Records         │                │
│                            └────────────────────────┘                │
│                                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
User Interaction
      │
      ▼
┌─────────────────────┐
│  Django URL Router  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐      ┌──────────────────────┐
│  View Function      │─────▶│  Database Query      │
└──────────┬──────────┘      └──────────┬───────────┘
           │                            │
           ▼                            ▼
┌─────────────────────┐      ┌──────────────────────┐
│  Template Rendering │      │  ORM Models          │
└──────────┬──────────┘      └──────────────────────┘
           │
           ▼
┌─────────────────────┐
│    HTML Response    │
└─────────────────────┘
```

### Application Modules

Educycle consists of **4 core Django applications**:

#### **1. Users Application** (`users/`)

User authentication, authorization, and profile management module.

**Responsibilities:**
- User registration and account creation
- Login/logout functionality
- Profile management and updates
- Phone number and email validation
- User data integrity

**Data Models:**
```python
User (Custom)
├── Username (unique)
├── Email (unique)
├── Phone Number (10-digit, unique)
├── First Name & Last Name
├── Password (hashed)
└── Timestamps (created_at, updated_at)
```

**Key Files:**
- `models.py` - User model extending AbstractUser
- `views.py` - Authentication views (signup, login, logout)
- `forms.py` - Registration and profile forms
- `urls.py` - User-related URL patterns
- `templates/` - User interface templates

---

#### **2. Items Application** (`items/`)

Product/item listing and inventory management module.

**Responsibilities:**
- Create and manage product listings
- Handle product images and metadata
- Track product availability status
- Manage product lifecycle (creation → sold/exchanged)

**Data Models:**
```python
Product
├── seller (ForeignKey → User)
├── title
├── description
├── price (decimal)
├── image (ImageField)
├── status (available, exchanged, sold)
├── created_at (timestamp)
└── updated_at (auto update)
```

**Status Workflow:**
```
available → exchanged/sold → inactive
```

**Key Files:**
- `models.py` - Product model definition
- `views.py` - Product CRUD operations
- `forms.py` - Product creation/edit forms
- `urls.py` - Product URL routing
- `templates/` - Product display templates

---

#### **3. Exchanges Application** (`exchanges/`)

Transaction management and order fulfillment module.

**Responsibilities:**
- Process exchange requests between users
- Track transaction status and history
- Enable buyer-seller communication
- Manage transaction lifecycle

**Data Models:**
```python
Exchange
├── product (ForeignKey → Product)
├── buyer (ForeignKey → User)
├── seller (ForeignKey → User)
├── status (pending, accepted, rejected, completed)
├── message (optional communication)
└── created_at (timestamp)
```

**Status Workflow:**
```
pending → accepted/rejected → completed
```

**Key Files:**
- `models.py` - Exchange model definition
- `views.py` - Exchange request and management views
- `urls.py` - Exchange URL routing
- `admin.py` - Django admin configuration

---

#### **4. Main/Core Application** (`Educycle/`)

Django project configuration and core settings.

**Responsibilities:**
- Global configuration management
- URL routing and middleware setup
- Database configuration
- Security settings
- Static and media file handling

**Key Files:**
- `settings.py` - Django settings with environment variables
- `urls.py` - Master URL configuration
- `wsgi.py` - Production WSGI entry point
- `asgi.py` - Async ASGI entry point

---

### Database Schema & Entity Relationships

```
┌─────────────────────┐
│      User           │
├─────────────────────┤
│ id (PK)             │
│ username (unique)   │
│ email (unique)      │
│ phone_number (U)    │
│ first_name          │
│ last_name           │
│ password (hashed)   │
│ is_active           │
│ created_at          │
└────────┬────────────┘
         │ (1:N)
         │
    ┌────┴────┐
    │          │
    ▼          ▼
┌─────────────┐  ┌──────────────────┐
│   Product   │  │    Exchange      │
├─────────────┤  ├──────────────────┤
│ id (PK)     │  │ id (PK)          │
│ seller_id(FK)  │  │ product_id(FK)   │
│ title       │  │ buyer_id(FK)     │
│ description │  │ seller_id(FK)    │
│ price       │  │ status           │
│ image       │  │ message (text)   │
│ status      │  │ created_at       │
│ created_at  │  │ updated_at       │
└─────────────┘  └──────────────────┘
```

**Key Relationships:**
- User (1) → Many Products (as seller)
- User (1) → Many Exchanges (as buyer)
- User (1) → Many Exchanges (as seller)
- Product (1) → Many Exchanges

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.11+ |
| **Web Framework** | Django | 5.2.10 |
| **Frontend** | HTML5/CSS3/JavaScript | - |
| **Template Engine** | Jinja2 | Built-in |
| **Database** | MySQL | 8.0+ |
| **ORM** | Django ORM | Built-in |
| **Image Processing** | Pillow | 10.1.0 |
| **Environment** | python-dotenv | 1.0.0 |
| **VCS** | Git | 2.0+ |

### Dependencies Breakdown

**Production Dependencies:**
- `Django==5.2.10` - Web framework
- `mysqlclient==2.2.0` - MySQL adapter
- `Pillow==10.1.0` - Image processing
- `python-dotenv==1.0.0` - Environment variables
- `pytz==2023.3` - Timezone support
- `sqlparse==0.4.4` - SQL parsing

See [requirements.txt](requirements.txt) for complete dependency list.

---

## Installation & Setup

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/yourusername/educycle.git
cd educycle
```

### **Step 2: Create Python Virtual Environment**
```bash
# Create virtual environment
python3 -m venv env

# Optional: Upgrade pip
pip install --upgrade pip
```

### **Step 3: Activate Virtual Environment**

**Linux / macOS:**
```bash
source env/bin/activate
```

**Windows (Command Prompt):**
```cmd
env\Scripts\activate
```

**Windows (PowerShell):**
```powershell
env\Scripts\Activate.ps1
```

### **Step 4: Install Python Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 5: Configure Environment Variables**

Create a `.env` file in the project root:

```env
# ============== Database Configuration ==============
DB_ENGINE=django.db.backends.mysql
DB_NAME=educycle
DB_USER=root
DB_PASSWORD=your_secure_password_here
DB_HOST=127.0.0.1
DB_PORT=3306

# ============== Django Settings ==============
SECRET_KEY=your_generated_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ============== Email Configuration (Optional) ==============
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

**Security Warning:** 
- Never commit `.env` to version control (it's in `.gitignore`)
- Use strong passwords for database and Django SECRET_KEY
- Generate SECRET_KEY using: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### **Step 6: Create MySQL Database**

```bash
# Login to MySQL
mysql -u root -p

# In MySQL prompt
CREATE DATABASE educycle CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

Or use MySQL Workbench/phpMyAdmin GUI.

### **Step 7: Run Database Migrations**

```bash
# Create migration files for new models
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

**Expected Output:**
```
Running migrations:
  Applying admin.001_initial... OK
  Applying auth.0001_initial... OK
  Applying users.0001_initial... OK
  Applying items.0001_initial... OK
  Applying exchanges.0001_initial... OK
```

### **Step 8: Create Superuser Account**

```bash
python manage.py createsuperuser
```

**Prompts:**
```
Username: admin
Email address: admin@example.com
Password: ****
Password (again): ****
Superuser created successfully.
```

### **Step 9: Collect Static Files (Production)**

```bash
python manage.py collectstatic --noinput
```

### **Step 10: Start Development Server**

```bash
python manage.py runserver
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**Access the Application:**
- Frontend: `http://localhost:8000/`
- Admin Panel: `http://localhost:8000/admin/`

---

## Configuration

### Environment Variables Reference

| Variable | Description | Example | Required |
|----------|-----------|---------|----------|
| `DB_ENGINE` | Database backend | `django.db.backends.mysql` | ✓ |
| `DB_NAME` | Database name | `educycle` | ✓ |
| `DB_USER` | Database user | `root` | ✓ |
| `DB_PASSWORD` | Database password | `password123` | ✓ |
| `DB_HOST` | Database host | `localhost` | ✓ |
| `DB_PORT` | Database port | `3306` | ✓ |
| `SECRET_KEY` | Django secret key | (auto-generated) | ✓ |
| `DEBUG` | Debug mode (dev only) | `True` | - |
| `ALLOWED_HOSTS` | Allowed domains | `localhost,127.0.0.1` | - |

### Django Settings Important Configurations

The following are configured in `Educycle/settings.py`:

- **Installed Apps**: users, items, exchanges
- **Middleware**: Security, session, auth, messages
- **Database**: MySQL via environment variables
- **Static Files**: CSS, JavaScript, images
- **Media Files**: User uploads (product images)
- **Authentication**: Custom User model with email

---

## Project Directory Structure

```
educycle/
│
├── Educycle/                          # Django core configuration
│   ├── __init__.py
│   ├── settings.py                    # Main Django settings
│   ├── urls.py                        # Root URL configuration
│   ├── wsgi.py                        # Production WSGI server entry
│   ├── asgi.py                        # Async ASGI server entry
│   └── __pycache__/
│
├── users/                             # User authentication app
│   ├── migrations/                    # Database migration files
│   ├── templates/
│   │   ├── base.html                 # Base template
│   │   ├── signup.html               # Registration page
│   │   ├── login.html                # Login page
│   │   └── profile.html              # User profile (future)
│   ├── __init__.py
│   ├── admin.py                      # Admin configuration
│   ├── apps.py                       # App configuration
│   ├── forms.py                      # User forms
│   ├── models.py                     # User model
│   ├── tests.py                      # Unit tests
│   ├── urls.py                       # App URL patterns
│   ├── views.py                      # View functions
│   └── __pycache__/
│
├── items/                             # Product listing app
│   ├── migrations/                    # Database migration files
│   ├── templates/
│   │   ├── dashboard.html            # Product dashboard
│   │   ├── addproducts.html          # Add product form
│   │   ├── productlist.html          # Products listing (future)
│   │   └── productdetail.html        # Product details (future)
│   ├── __init__.py
│   ├── admin.py                      # Admin configuration
│   ├── apps.py                       # App configuration
│   ├── forms.py                      # Product forms
│   ├── models.py                     # Product model
│   ├── tests.py                      # Unit tests
│   ├── urls.py                       # App URL patterns
│   ├── views.py                      # View functions
│   └── __pycache__/
│
├── exchanges/                         # Transaction management app
│   ├── migrations/                    # Database migration files
│   ├── __init__.py
│   ├── admin.py                      # Admin configuration
│   ├── apps.py                       # App configuration
│   ├── models.py                     # Exchange model
│   ├── tests.py                      # Unit tests
│   ├── urls.py                       # App URL patterns
│   ├── views.py                      # View functions
│   └── __pycache__/
│
├── media/                             # User-uploaded files
│   └── product_images/               # Product image storage
│
├── static/                            # Static assets (CSS, JS, images)
│   ├── css/                          # Stylesheets
│   ├── js/                           # JavaScript files
│   └── icons/                        # Icon assets
│
├── templates/                         # Global templates
│   └── home.html                     # Homepage
│
├── db.sqlite3                        # SQLite database (development)
├── manage.py                         # Django management command
├── requirements.txt                  # Python dependencies
├── .env                              # Environment variables (not in git)
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
├── README.md                         # This file
└── LICENSE                           # MIT License
```

---
## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---