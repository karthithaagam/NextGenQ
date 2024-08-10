from django.core.mail import send_mail
from django.conf import settings
import django

# Setup Django settings
settings.configure(
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend",
    EMAIL_USE_TLS = True,
    EMAIL_HOST = "mail.thaagam.email",
    EMAIL_PORT = 587,
    EMAIL_USE_SSL = False,
    EMAIL_HOST_USER = "office@acustomsong.com",
    EMAIL_HOST_PASSWORD="6FOEnk{}#jcc",
    DEFAULT_FROM_EMAIL = "office@acustomsong.com",
)

django.setup()

# Send the email
send_mail(
    'Test Email',
    'This is a test email from Django.',
    'office@acustomsong.com',
    ['karthithaagam@gmail.com'],
    fail_silently=False,
)
print("Email sent successfully!")
