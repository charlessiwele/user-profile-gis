from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User


class Command(BaseCommand):
    help = 'Assigns existing staff users (non-superusers) to the Staff group'

    def handle(self, *args, **options):
        # Get or create the Staff group
        try:
            staff_group = Group.objects.get(name='Staff')
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                '✗ Staff group does not exist. Run "python manage.py create_staff_group" first.'
            ))
            return
        
        # Get all staff users who are not superusers and not already in the group
        staff_users = User.objects.filter(
            is_staff=True,
            is_superuser=False
        ).exclude(groups=staff_group)
        
        if not staff_users.exists():
            self.stdout.write(self.style.WARNING(
                '→ No staff users found that need to be assigned to the group.'
            ))
            return
        
        # Assign users to the group
        count = 0
        for user in staff_users:
            user.groups.add(staff_group)
            count += 1
            self.stdout.write(self.style.SUCCESS(
                f'✓ Added {user.username} to Staff group'
            ))
        
        # Show summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS(
            f'Successfully assigned {count} user(s) to Staff group'
        ))
        self.stdout.write(self.style.SUCCESS('='*60))

