from django.core.management.base import BaseCommand
from django.utils import timezone
from land_management.models import Approval

class Command(BaseCommand):
    help = 'Backfill approval date fields for already-approved records with missing dates.'

    def handle(self, *args, **options):
        updated = 0
        now = timezone.now().date()
        approvals = Approval.objects.all()
        for approval in approvals:
            changed = False
            if approval.director_status == 'approved' and not approval.director_approval_date:
                approval.director_approval_date = now
                changed = True
            if approval.secretary_status == 'approved' and not approval.secretary_approval_date:
                approval.secretary_approval_date = now
                changed = True
            if approval.deputy_mayor_status == 'approved' and not approval.deputy_mayor_approval_date:
                approval.deputy_mayor_approval_date = now
                changed = True
            if approval.mayor_status == 'approved' and not approval.mayor_approval_date:
                approval.mayor_approval_date = now
                changed = True
            if changed:
                approval.save()
                updated += 1
        self.stdout.write(self.style.SUCCESS(f'Backfilled {updated} approval records.')) 