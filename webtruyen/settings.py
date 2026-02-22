import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 1. SECURITY (BẢO MẬT) ---
# Lấy SECRET_KEY từ biến môi trường của Render
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-15&9bm1ik@+8py!xjzxn&6k3_td#8mi79wq-#m4df%bz(0$3r7')

# Tự động tắt DEBUG khi lên Render, bật khi chạy ở máy (Local)
DEBUG = 'RENDER' not in os.environ

# --- 2. HOST CONFIG (CẤU HÌNH TÊN MIỀN) ---
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Tự động lấy tên miền từ Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# --- 3. APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'jazzmin', # Phải nằm trên cùng
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Hỗ trợ file tĩnh khi DEBUG=False
    'django.contrib.staticfiles',
    'cloudinary', 
    'story',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Phải nằm ngay dưới SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webtruyen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webtruyen.wsgi.application'

# --- 4. DATABASE (CẤU HÌNH KẾT NỐI SSL CHO RENDER) ---
DATABASES = {
    'default': dj_database_url.config(
        # Link database local (dùng khi chạy máy nhà)
        default='postgresql://postgres:1234@localhost:5432/webtruyen',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# QUAN TRỌNG: Bắt buộc dùng SSL khi chạy trên Render để tránh lỗi 500
if 'RENDER' in os.environ:
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'require',
    }

# --- 5. STATIC & MEDIA (FILE TĨNH & ẢNH) ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Cấu hình lưu trữ mới cho Django 5.x (Thay thế STATICFILES_STORAGE cũ)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- 6. CLOUDINARY CONFIG ---
CLOUDINARY_CLOUD_NAME = 'dqb9trxs4'
CLOUDINARY_API_KEY = '526277124128331'
CLOUDINARY_API_SECRET = 'lBNZfs38GP1iGvMKXCRzjDzZcss'

import cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

# --- 7. JAZZMIN UI CONFIG ---
JAZZMIN_SETTINGS = {
    "site_title": "Thiên Mộng Hành Admin",
    "site_header": "Thiên Mộng Hành",
    "site_brand": "Quản trị Nguyệt Mộng",
    "welcome_sign": "Chào mừng bạn đến với hệ thống quản trị truyện",
    "copyright": "Thiên Mộng Hành Ltd",
    "search_model": ["story.Story"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "story.Story": "fas fa-book",
        "story.Category": "fas fa-list",
        "story.Chapter": "fas fa-file-alt",
        "story.Comment": "fas fa-comments",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar_variant": "navbar-dark",
    "accent": "accent-primary",
}

# --- 8. KHÁC ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'