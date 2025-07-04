from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            email="admin@example.com",
            first_name="admin",
            last_name="admin",
        )

        user.set_password("1234qwe")

        user.is_staff = True
        user.is_superuser = True

        user.save()

        self.stdout.write(self.style.SUCCESS(f"Успешно создан суперадмин {user.email}"))
