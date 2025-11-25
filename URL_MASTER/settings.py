from pathlib import Path
import os

# Base directory of the project (folder containing manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# For now it's hard-coded; later you can move it to environment variables.
SECRET_KEY = "f9k2uc+)@c(@4k!_2v3a+83bqe8##(f8ul8%uk(@-jf77h8a6$"

# DEBUG:
# - True  -> for local development (more error details)
# - False -> for production (public hosting)
DEBUG = False  # set True while developing locally if you want

# When DEBUG=False, Django only serves requests for hosts listed here.
# In production: put your Render / PythonAnywhere domain here.
# Example: ["your-app.onrender.com", "localhost", "127.0.0.1"]
ALLOWED_HOSTS = ["*"]  # keep "*" while testing; lock down later in real prod


# --------------------------------------------------------------------
# Installed apps
# --------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Your app
    "urlmaster",
]


# --------------------------------------------------------------------
# Middleware
# --------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# --------------------------------------------------------------------
# URL configuration
# --------------------------------------------------------------------
ROOT_URLCONF = "URL_MASTER.urls"


# --------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        # Global templates folder (optional).
        # You are using app templates (urlmaster/templates), which works
        # because APP_DIRS = True. This DIRS entry is fine and optional.
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],

        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# --------------------------------------------------------------------
# WSGI application
# --------------------------------------------------------------------
WSGI_APPLICATION = "URL_MASTER.wsgi.application"


# --------------------------------------------------------------------
# Database (SQLite for now)
# --------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# --------------------------------------------------------------------
# Password validation
# --------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --------------------------------------------------------------------
# Internationalization
# --------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"

USE_I18N = True
USE_TZ = True


# --------------------------------------------------------------------
# Static files (CSS, JS, images)
# --------------------------------------------------------------------
STATIC_URL = "/static/"

# This is where 'collectstatic' will put all static files for production.
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# OPTIONAL for dev: if you want a global /static folder in your project root,
# create a folder named "static" in BASE_DIR and uncomment this.
# Leaving it commented avoids the staticfiles.W004 warning.
#
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]


# --------------------------------------------------------------------
# Default primary key field type
# --------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
