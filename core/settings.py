"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import environ


env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = []


# Application definition

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'index',
    'users',
    'categories',
    'products',
    'cart'
]


THIRD_PARTY_APPS = [
    'six',
    'tinymce',
]


INSTALLED_APPS = DEFAULT_APPS + PROJECT_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/El_Salvador'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CUSTOM USER
AUTH_USER_MODEL = "users.CustomUser"


# ACTIVATE EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
PASSWORD_RESET_TIMEOUT = 1440


# CONFIG TINYMCE
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
TINYMCE_DEFAULT_CONFIG = {
    "skin": 'oxide-dark',
    "custom_undo_redo_levels": 100,
    "selector": "textarea",
    "menubar": "file edit view insert format tools table help",
    "plugins": "link image preview codesample contextmenu table code lists fullscreen textcolor emoticons",
    "toolbar1": "undo redo | backcolor forecolor casechange permanentpen formatpainter removeformat formatselect fontselect fontsizeselect",
    "toolbar2": "bold italic underline blockquote | alignleft aligncenter alignright alignjustify "
    "| bullist numlist | outdent indent | table | link image | codesample | preview code | tiny_mce_wiris_formulaEditor tiny_mce_wiris_formulaEditorChemistry",
    "contextmenu": "formats | link image",
    "block_formats": "Paragraph=p; Header 1=h1; Header 2=h2",
    "fontsize_formats": "8pt 10pt 12pt 14pt 16pt 18pt",
    "file_picker_types": 'image',
    "image_class_list": [{"title": "Fluid", "value": "img-fluid", "style": {}}],
    "width": "100%",
    "height": "600px",
    "image_caption": True,
    "content_css": [
        'https://cdn.jsdelivr.net/npm/prismjs@1.24.1/themes/prism.css'
    ],

    "setup": """function (editor) {
    editor.on('init', function () {
      editor.contentDocument.body.classList.add('language-markup'); 
    });
    }""",
    "file_picker_callback": """
        function (cb, value, meta) {
            var input = document.createElement('input');
            input.setAttribute('type', 'file');
            input.setAttribute('accept', 'image/*');

            input.onchange = function () {
                var file = this.files[0];

                var reader = new FileReader();
                reader.onload = function () {
                    var id = 'blobid' + (new Date()).getTime();
                    var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                    var base64 = reader.result.split(',')[1];
                    var blobInfo = blobCache.create(id, file, base64);
                    blobCache.add(blobInfo);

                    cb(blobInfo.blobUri(), { title: file.name });
                };
                reader.readAsDataURL(file);
            };
            input.click();
        }
    """,
    "content_style": "body { font-family: Arial; background: rgb(32, 45, 83); color: white; font-size: 12pt}",
    "codesample_languages": [
        {"text": "HTML/XML", "value": "markup"},
        {"text": "JavaScript", "value": "javascript"},
        {"text": "CSS", "value": "css"},
        {"text": "PHP", "value": "php"},
        {"text": "Ruby", "value": "ruby"},
        {"text": "Python", "value": "python"},
        {"text": "Java", "value": "java"},
        {"text": "C", "value": "c"},
        {"text": "C#", "value": "csharp"},
        {"text": "C++", "value": "cpp"},
        {"text": "Bash/Shell", "value": "bash"},
        {"text": "CoffeeScript", "value": "coffeescript"},
        {"text": "Diff", "value": "diff"},
        {"text": "Erlang", "value": "erlang"},
        {"text": "Groovy", "value": "groovy"},
        {"text": "JSON", "value": "json"},
        {"text": "Less", "value": "less"},
        {"text": "Makefile", "value": "makefile"},
        {"text": "Markdown", "value": "markdown"},
        {"text": "Objective-C", "value": "objectivec"},
        {"text": "R", "value": "r"},
        {"text": "Sass", "value": "sass"},
        {"text": "SCSS", "value": "scss"},
        {"text": "SQL", "value": "sql"},
        {"text": "TypeScript", "value": "typescript"},
        {"text": "YAML", "value": "yaml"}
    ],
}
