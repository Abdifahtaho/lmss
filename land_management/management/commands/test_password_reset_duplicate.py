from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from land_management.models import PasswordResetRequest
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Test password reset duplicate prevention functionality'

    def handle(self, *args, **options):
        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created test user: {user.username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Using existing test user: {user.username}'))
        
        # Test 1: Check if user has pending request
        pending_request = PasswordResetRequest.get_pending_request(user)
        if pending_request:
            self.stdout.write(self.style.WARNING(f'User has pending request from: {pending_request.requested_at}'))
        else:
            self.stdout.write(self.style.SUCCESS('No pending request found'))
        
        # Test 2: Create a pending request
        reset_request = PasswordResetRequest.objects.create(
            user=user,
            rejection_reason='Test request'
        )
        self.stdout.write(self.style.SUCCESS(f'Created password reset request: {reset_request.id}'))
        
        # Test 3: Check again for pending request
        pending_request = PasswordResetRequest.get_pending_request(user)
        if pending_request:
            self.stdout.write(self.style.SUCCESS(f'Found pending request: {pending_request.id} from {pending_request.requested_at}'))
        else:
            self.stdout.write(self.style.ERROR('No pending request found after creation'))
        
        # Test 4: Test the has_pending_request method
        has_pending = reset_request.has_pending_request()
        self.stdout.write(self.style.SUCCESS(f'has_pending_request() returns: {has_pending}'))
        
        # Test 5: Create an old request (more than 24 hours ago)
        old_request = PasswordResetRequest.objects.create(
            user=user,
            requested_at=timezone.now() - timedelta(hours=25),
            status='pending',
            rejection_reason='Old test request'
        )
        self.stdout.write(self.style.SUCCESS(f'Created old request: {old_request.id}'))
        
        # Test 6: Check pending requests again
        pending_request = PasswordResetRequest.get_pending_request(user)
        if pending_request:
            self.stdout.write(self.style.SUCCESS(f'Most recent pending request: {pending_request.id} from {pending_request.requested_at}'))
        
        # Clean up old test requests
        PasswordResetRequest.objects.filter(user=user, rejection_reason__startswith='Test').delete()
        self.stdout.write(self.style.SUCCESS('Cleaned up test requests')) 