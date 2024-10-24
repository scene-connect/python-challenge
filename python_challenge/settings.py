import importlib.metadata
import logging
import os
from pathlib import Path

import structlog
from corsheaders.defaults import default_headers
from dotenv import load_dotenv

load_dotenv()
load_dotenv("/app/secrets/.env")


BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
ALLOW_LOCALHOST = bool(os.environ.get("ALLOW_LOCALHOST", False))

# Security.
DOMAIN_NAME: str = os.environ.get("DOMAIN_NAME", "pyhon-challenge.zuos.co.uk")
ALLOWED_HOSTS: list[str] = [DOMAIN_NAME]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [f"https://{DOMAIN_NAME}"]
CORS_ALLOW_HEADERS = (
    *default_headers,
    "sentry-trace",
    "baggage",
)
CORS_EXPOSE_HEADERS = ("senty-trace", "baggage")
CORS_ALLOW_ALL_ORIGINS = True

CSRF_COOKIE_DOMAIN: str | None = DOMAIN_NAME
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    f"https://{DOMAIN_NAME}",
]

# the secret key gets set from an environment variable anyway sot he default is fine.
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-n8--1$%0b9($55pl0a+!%9&nt7(vihpc=y2u6tw!8_g)7^s@=^"
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_SECONDS = 3600  # TODO increase soon after production deployment

SESSION_COOKIE_SECURE = True

DEBUG = os.environ.get("DEBUG") == "1"

if ENVIRONMENT == "development" or ALLOW_LOCALHOST:  # pragma: no cover
    ALLOWED_HOSTS.append("localhost")
    ALLOWED_HOSTS.append("127.0.0.1")  # Allows using the django runserver url.
if ENVIRONMENT == "development":  # pragma: no cover
    CSRF_COOKIE_DOMAIN = None
    SECURE_HSTS_SECONDS = 0
    dev_url = f"https://localhost:{os.environ.get('PORT', 8000)}"
    dev_nextjs_url = "https://localhost:3000"
    CSRF_TRUSTED_ORIGINS.append(dev_url)
    CSRF_TRUSTED_ORIGINS.append(dev_url)
    CORS_ALLOWED_ORIGINS = [dev_url, dev_nextjs_url]

CSP_SCRIPT_SRC = [
    "'self'",
    "cdn.jsdelivr.net",
]

CSP_STYLE_SRC = [
    "'self'",
    "cdn.jsdelivr.net",
    "'unsafe-inline'",
]


# Django Rest Framework

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Python Challenge API - Documentation",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "VERSION": importlib.metadata.version("python-challenge"),
    "TAGS": [],
    "POSTPROCESSING_HOOKS": [
        # Use DRF-spectacular's default enum processing hook.
        "drf_spectacular.hooks.postprocess_schema_enums",
    ],
}


# Application definition.

APPEND_SLASH = False


INSTALLED_APPS = [
    "python_challenge.docs.apps.DocsConfig",
    "python_challenge.api.apps.ApiConfig",
    "corsheaders", 
    "debug_toolbar",
    "rest_framework",
    "drf_spectacular",
    "django_extensions",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "csp.middleware.CSPMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
]


ROOT_URLCONF = "python_challenge.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "python_challenge.wsgi.application"


# Internationalization.

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True


# Static files.

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "static/"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

# System checks.
SILENCED_SYSTEM_CHECKS = [
    # Username field must be unique -- we use a custom unique constraint.
    "auth.E003",
    # SECURE_SSL_REDIRECT -- seems to break Cloud Run and is handled there.
    "security.W008",
]


# Logging & reporting.

# Structlog processors shared with the logging formatter.
_shared_processors: list[structlog.typing.Processor] = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
]

# Structlog-only processors
_structlog_processors: list[structlog.typing.Processor] = [
    structlog.stdlib.filter_by_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.format_exc_info,
    structlog.processors.StackInfoRenderer(),
    structlog.processors.UnicodeDecoder(),
]


def _logging_google_cloud_map(
    logger: logging.Logger, function_name: str, event_dict: structlog.typing.EventDict
) -> structlog.typing.EventDict:  # pragma: no cover
    if "message" not in event_dict and "event" in event_dict:
        event_dict["message"] = event_dict.pop("event")
    if "severity" not in event_dict:
        event_dict["severity"] = event_dict["level"].upper()
    return event_dict


structlog.configure(
    processors=(
        _shared_processors
        + _structlog_processors
        + [
            _logging_google_cloud_map,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ]
    ),
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

_logging_renderer: structlog.typing.Processor
if ENVIRONMENT == "development":  # pragma: no cover
    _logging_renderer = structlog.dev.ConsoleRenderer()
else:  # pragma: no cover
    _logging_renderer = structlog.processors.JSONRenderer()

_logging_formatter = structlog.stdlib.ProcessorFormatter(
    # Foreign pre-chain processors run only on log entries not from structlog
    foreign_pre_chain=_shared_processors + [_logging_google_cloud_map],
    processors=[
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        _logging_renderer,
    ],
)
_logging_handler = logging.StreamHandler()
_logging_handler.setFormatter(_logging_formatter)
logging.getLogger("httpx").setLevel(logging.INFO)
logging.getLogger("httpcore").setLevel(logging.INFO)
_root_logger = logging.getLogger()
_root_logger.addHandler(_logging_handler)
_root_logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))
