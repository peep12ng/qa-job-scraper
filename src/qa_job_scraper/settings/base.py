import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BASE_DIR.parent

def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value

def get_env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and (value is None or value == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

def get_env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")

load_dotenv(PROJECT_ROOT / ".env")

APP_ENV = get_env("APP_ENV", default="local")

SECRET_KEY = get_env("DJANGO_SECRET_KEY", required=True)
DEBUG = get_env_bool("DJANGO_DEBUG", default=(APP_ENV == "local"))

ALLOWED_HOSTS = [
    host.strip()
    for host in get_env("DJANGO_ALLOWED_HOSTS", default="").split(",")
    if host.strip()
]

LOG_DIR = Path(get_env("LOG_DIR", default=str(PROJECT_ROOT / "logs")))
LOG_DIR.mkdir(parents=True, exist_ok=True)

DB_ENGINE = get_env("DB_ENGINE", default="mysql", required=True)
if DB_ENGINE == "mysql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': get_env("DB_NAME", required=True),
            'USER': get_env("DB_USER", required=True),
            'PASSWORD': get_env("DB_PASSWORD", required=True),
            'HOST': get_env("DB_HOST", required=True),
            'PORT': get_env("DB_PORT", required=True),
        }
    }
elif DB_ENGINE == "sqlite":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    raise RuntimeError(f"Unsupported DB_ENGINE: {DB_ENGINE}")

SCRAPE_INTERVAL_HOURS = int(get_env("SCRAPE_INTERVAL_HOURS", required=True))
SCRAPE_TIMEZONE = get_env("SCRAPE_TIMEZONE", required=True)

PLAYWRIGHT_BROWSER = get_env("PLAYWRIGHT_BROWSER", required=True)
PLAYWRIGHT_HEADLESS = get_env_bool("PLAYWRIGHT_HEADLESS", default=True)
PLAYWRIGHT_TIMEOUT_MS = int(get_env("PLAYWRIGHT_TIMEOUT_MS", default="30000"))

CELERY_BROKER_URL = get_env("CELERY_BROKER_URL", default=None)
CELERY_RESULT_BACKEND = get_env("CELERY_RESULT_BACKEND", default=None)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "jobs",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'qa_job_scraper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'qa_job_scraper.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": str(LOG_DIR / "app.log"),
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
