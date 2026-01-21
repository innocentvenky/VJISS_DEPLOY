import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create admin (superuser) from environment variables if not exists"

    def handle(self, *args, **options):
        User = get_user_model()

        # Required ENV vars
        email = os.getenv("DJANGO_ADMIN_EMAIL")
        password = os.getenv("DJANGO_ADMIN_PASSWORD")

        if not email or not password:
            self.stdout.write(self.style.ERROR(
                "❌ DJANGO_ADMIN_EMAIL or DJANGO_ADMIN_PASSWORD not set"
            ))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(
                "ℹ Admin user already exists"
            ))
            return

        # Optional ENV vars
        first_name = os.getenv("DJANGO_ADMIN_FIRST_NAME")

        phone_raw = os.getenv("DJANGO_ADMIN_PHONE")
        phone = int(phone_raw) if phone_raw else None

        dob_raw = os.getenv("DJANGO_ADMIN_DOB")
        dob = (
            datetime.strptime(dob_raw, "%Y-%m-%d").date()
            if dob_raw else None
        )

        # Create superuser
        User.objects.create_superuser(
            email=email,
            password=password,
            first_name=first_name,
            phone_number=phone,
            date_of_birth=dob,
        )

        self.stdout.write(self.style.SUCCESS(
            "✅ Admin superuser created successfully"
        ))
