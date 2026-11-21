import os
from pathlib import Path

import dj_database_url
from corsheaders.defaults import default_headers
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-chave-local-genios")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Bibliotecas de terceiros
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "corsheaders",
    # Apps do GeniOS
    "nucleo",
    "importacao",
    "almoxarifado",
    "dados_demo",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(",")
# O filtro global de polo viaja no cabeçalho X-Polo-Id (contrato §1).
CORS_ALLOW_HEADERS = (*default_headers, "x-polo-id")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["nucleo.autenticacao.TokenBearerComValidade"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "EXCEPTION_HANDLER": "nucleo.tratamento_erros.tratar_excecao",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "GeniOS API",
    "DESCRIPTION": "API do MVP do GeniOS. Contrato de referência: docs/contrato-api.md.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# HU-001 RN-L02: planilha de até 25 MiB. O Django precisa aceitar o corpo para o service
# responder 413 com mensagem clara em vez de um erro genérico.
LIMITE_PLANILHA_BYTES = 25 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = LIMITE_PLANILHA_BYTES + 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = LIMITE_PLANILHA_BYTES + 1024 * 1024

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
