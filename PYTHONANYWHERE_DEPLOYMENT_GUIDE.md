# Educycle - PythonAnywhere Deployment Guide

Your Django application is now production-ready. Follow these steps to deploy on PythonAnywhere.

---

## ✅ Completed Setup on Local Machine

- [x] `DEBUG = False` in settings.py
- [x] `ALLOWED_HOSTS = ['mothishraghavendra.pythonanywhere.com', 'localhost', '127.0.0.1']`
- [x] `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')` configured
- [x] `collectstatic` executed (138 static files collected)
- [x] `requirements.txt` updated with pip freeze
- [x] Database configured to use environment variables

---

## 📤 Step 1: Upload to GitHub (Recommended)

```bash
git init
git add .
git commit -m "Production ready for PythonAnywhere deployment"
git remote add origin https://github.com/yourusername/educycle.git
git push -u origin main
```

Or upload the zip file directly via PythonAnywhere Files tab.

---

## 🐍 Step 2: Create Virtual Environment on PythonAnywhere

In PythonAnywhere Bash console:

```bash
mkvirtualenv --python=/usr/bin/python3.10 educycle_env
pip install -r requirements.txt
```

---

## ⚙️ Step 3: Configure Web App

1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose:
   - **Python 3.10** (or your version)
   - **Manual configuration** (NOT Flask/Django pre-configured)

---

## 🧠 Step 4: Edit WSGI File (CRITICAL!)

1. In Web tab, under **Code** section, click the WSGI configuration file
2. Replace it with:

```python
import sys
import os
from pathlib import Path

# Add project to path
path = '/home/mothishraghavendra/educycle'  # Change 'mothishraghavendra' to your username
if path not in sys.path:
    sys.path.insert(0, path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'Educycle.settings'

# Activate virtual environment
virtualenv = '/home/mothishraghavendra/.virtualenvs/educycle_env/lib/python3.10/site-packages'
if virtualenv not in sys.path:
    sys.path.insert(0, virtualenv)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## 🗄️ Step 5: Database Configuration

### If using your remote MySQL database:

1. Create `.env` file in `/home/yourusername/educycle/`:

```
DB_ENGINE=django.db.backends.mysql
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host.aivencloud.com
DB_PORT=12418

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

2. Run migrations in Bash console:

```bash
cd /home/yourusername/educycle
source /home/yourusername/.virtualenvs/educycle_env/bin/activate
python manage.py migrate
python manage.py createsuperuser
```

### If using SQLite (local):

```bash
cd /home/yourusername/educycle
source /home/yourusername/.virtualenvs/educycle_env/bin/activate
python manage.py migrate
python manage.py createsuperuser
```

---

## 📁 Step 6: Configure Static Files

In Web tab → **Static files** section:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/educycle/staticfiles` |
| `/media/` | `/home/yourusername/educycle/media` |

---

## 🚀 Step 7: Reload Web App

Click **Reload** button in Web tab.

Then visit: **https://mothishraghavendra.pythonanywhere.com**

---

## ⚠️ Troubleshooting

### Error: ModuleNotFoundError
- Make sure virtualenv path is correct in WSGI file
- Username in path must match your PythonAnywhere username

### Error: Static files not loading
- Run `python manage.py collectstatic --noinput` in bash
- Check Static files configuration in Web tab

### Error: Database connection failed
- Verify `.env` file exists and has correct credentials
- Check database is accessible from PythonAnywhere IP

### Error: 500 Internal Server Error
- Check Error log in Web tab
- Verify `DEBUG = False` in settings.py
- Ensure all dependencies are installed in virtualenv

---

## 📝 Additional Notes

- Your `DEBUG = False` - no debug page in production (check error logs)
- Secret key is in `settings.py` - consider using environment variable
- Static files served from `staticfiles/` directory
- Media files from `media/` directory
- Database credentials stored in `.env` (not in version control)

---

## ✨ Environment Variables to Add (if not in .env)

PythonAnywhere → Account → Web app → Environment variables:

```
DB_ENGINE=django.db.backends.mysql
DB_NAME=database_name
DB_USER=username
DB_PASSWORD=password
DB_HOST=your-host.com
DB_PORT=12418
```

Or add file-based `.env` in your project root.

---

Good luck with your deployment! 🚀
