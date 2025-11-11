from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app.models import UserProfile


class Command(BaseCommand):
    help = 'Creates a Staff group with permissions to view and edit UserProfile'

    def handle(self, *args, **options):
        # Get or create the Staff group
        staff_group, created = Group.objects.get_or_create(name='Staff')
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created "Staff" group'))
        else:
            self.stdout.write(self.style.WARNING('→ "Staff" group already exists'))
        
        # Get the UserProfile content type
        content_type = ContentType.objects.get_for_model(UserProfile)
        
        # Define the permissions we want to assign
        permission_codenames = [
            'view_userprofile',
            'change_userprofile',
        ]
        
        # Get the permissions
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=permission_codenames
        )
        
        # Clear existing permissions and add new ones
        staff_group.permissions.clear()
        staff_group.permissions.add(*permissions)
        
        self.stdout.write(self.style.SUCCESS(
            f'✓ Assigned {permissions.count()} permissions to "Staff" group:'
        ))
        
        for perm in permissions:
            self.stdout.write(f'  - {perm.codename}: {perm.name}')
        
        # Show summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Staff Group Configuration Complete!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'Group Name: {staff_group.name}')
        self.stdout.write(f'Permissions: {staff_group.permissions.count()}')
        self.stdout.write('\nUsers in this group can:')
        self.stdout.write('  ✓ View UserProfile model in admin')
        self.stdout.write('  ✓ Edit UserProfile records')
        self.stdout.write('\nNote: Admin permissions will restrict non-superuser')
        self.stdout.write('      staff to only see/edit their own profile.')

