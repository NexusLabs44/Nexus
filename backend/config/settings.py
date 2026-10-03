from pathlib import Path

from decouple import config, Csv


# ============================================================
# BASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SEGURANÇA
# ============================================================

SECRET_KEY = config(
    "DJANGO_SECRET_KEY"
)

DEBUG = config(
    "DJANGO_DEBUG",
    default=False,
    cast=bool,
)

ALLOWED_HOSTS = config(
    "DJANGO_ALLOWED_HOSTS",
    default="127.0.0.1,localhost",
    cast=Csv(),
)


# ============================================================
# APLICAÇÕES
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # CORS
    "corsheaders",

    # Aplicações do projeto
    "accounts",
    "calculations",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Deve ficar antes do CommonMiddleware
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URLS / WSGI
# ============================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR.parent / "frontend" / "pages",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ============================================================
# BANCO DE DADOS
# ============================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",

        "NAME": config(
            "DB_NAME"
        ),

        "USER": config(
            "DB_USER"
        ),

        "PASSWORD": config(
            "DB_PASSWORD"
        ),

        "HOST": config(
            "DB_HOST"
        ),

        "PORT": config(
            "DB_PORT",
            cast=int,
        ),

        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}


# ============================================================
# USUÁRIO
# ============================================================

AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/perfil/"

LOGOUT_REDIRECT_URL = "/login/"


# ============================================================
# VALIDAÇÃO DE SENHA
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ============================================================
# INTERNACIONALIZAÇÃO
# ============================================================

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Recife"

USE_I18N = True

USE_TZ = True


# ============================================================
# ARQUIVOS ESTÁTICOS
# ============================================================

STATIC_URL = "/assets/"

STATICFILES_DIRS = [
    BASE_DIR.parent / "frontend" / "assets",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# CORS
# ============================================================

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default=(
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "https://nexus-frontend-murex-two.vercel.app"
    ),
    cast=Csv(),
)

CORS_ALLOW_CREDENTIALS = True


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default=(
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "https://nexus-frontend-murex-two.vercel.app"
    ),
    cast=Csv(),
)


# ============================================================
# SEGURANÇA HTTPS
# ============================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


# ============================================================
# SESSÃO / COOKIES
# ============================================================

SESSION_COOKIE_SECURE = not DEBUG

SESSION_COOKIE_SAMESITE = "None"

CSRF_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SAMESITE = "None"

