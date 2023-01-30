from pathlib import Path
import datetime
import os

def read_secret(secret_name):
    with open(f'.secrets/{secret_name}', 'r') as f:
        secret = f.read().strip()
    return secret

def read_env(env_name):
    with open(f'.env/{env_name}', 'r') as f:
        env = f.read().strip()
    return env


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = read_secret('BACKEND_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '13.125.166.128',
    'apis.opendata-finance-kr.com',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps
    'api',
    'marketdata',

    # third parties
    'rest_framework',
    'corsheaders',
]

WSGI_APPLICATION = 'config.wsgi.application'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DEV_FRONTEND_BASE_URL = read_env('DEV_FRONTEND_BASE_URL')
CORS_ALLOWED_ORIGINS = [
    'http://www.opendata-finance-kr.com',
    DEV_FRONTEND_BASE_URL,
]

ROOT_URLCONF = 'config.urls'

DATABASES = {
    'default': {},
    'marketdata_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'marketdata',
        'USER': 'admin',
        'PASSWORD': read_secret('AWS_RDS_PASSWORD'),
        'HOST': 'opendata-finance-kr-marketdata.cai2wlj5r9yu.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
    'primary': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

DATABASE_ROUTERS = [
    'config.db_routers.MarketdataRouter',
    'config.db_routers.PrimaryRouter',
]

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

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'

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
