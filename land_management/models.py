from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import re
from django.core.exceptions import ValidationError
from django.utils import timezone

# Custom Validators

def validate_national_id(value):
    if not re.match(r'^[0-9]{6,20}$', value):
        raise ValidationError('National ID must be 6-20 digits.')

def validate_phone_number(value):
    if not re.match(r'^\+?[0-9]{7,15}$', value):
        raise ValidationError('Phone number must be 7-15 digits and may start with +.')

def validate_alpha_name(value):
    if not re.match(r'^[A-Za-z ]+$', value):
        raise ValidationError('Name must contain only letters and spaces.')

class LandRegistration(models.Model):
    REGISTRATION_TYPE_CHOICES = [
        ('sale', 'Land Sale'),
        ('gift', 'Gift Land'),
        ('inheritance', 'Inheritance'),
        ('exchange', 'Land Exchange'),
        ('donation', 'Donation'),
        ('court_order', 'Court Order'),
        ('government_allocation', 'Government Allocation'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    LAND_SIZE_CHOICES = [
        ('6x12', '6x12'),
        ('9x12', '9x12'),
        ('custom', 'Custom'),
    ]
    
    LAND_USE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('agricultural', 'Agricultural'),
    ]
    
    DIRECTION_TYPE_CHOICES = [
        ('building', 'Building'),
        ('road', 'Road'),
        ('empty', 'Empty'),
    ]
    
    # Registration Type
    registration_type = models.CharField(max_length=30, choices=REGISTRATION_TYPE_CHOICES, default='sale')
    
    # Basic Information
    transaction_reference = models.CharField(max_length=20, unique=True)
    date_of_sale = models.DateField()
    register_date = models.DateField(auto_now_add=True)
    sale_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # Optional for non-sale types
    
    # Seller/Transferor Information
    seller_full_name = models.CharField(max_length=255, validators=[validate_alpha_name])
    seller_national_id = models.CharField(max_length=50, validators=[validate_national_id])
    seller_birth_date = models.DateField()
    seller_phone = models.CharField(max_length=20, validators=[validate_phone_number])
    seller_address = models.TextField(blank=True, null=True)
    
    # Buyer/Transferee Information
    buyer_full_name = models.CharField(max_length=255, validators=[validate_alpha_name])
    buyer_national_id = models.CharField(max_length=50, validators=[validate_national_id])
    buyer_phone = models.CharField(max_length=20, validators=[validate_phone_number])
    buyer_address = models.TextField(blank=True, null=True)
    
    # Land Information
    land_code = models.CharField(max_length=20, unique=True)
    land_size = models.CharField(max_length=10)  # Allow any value
    size_unit = models.CharField(max_length=10, default='sqm', blank=True)
    land_zone = models.CharField(max_length=100)
    land_district = models.CharField(max_length=100)
    land_region = models.CharField(max_length=100)
    land_use_type = models.CharField(max_length=20, choices=LAND_USE_CHOICES)
    
    # Land Direction Information
    land_direction_east = models.CharField(max_length=20, choices=DIRECTION_TYPE_CHOICES, blank=True, null=True)
    land_direction_south = models.CharField(max_length=20, choices=DIRECTION_TYPE_CHOICES, blank=True, null=True)
    land_direction_west = models.CharField(max_length=20, choices=DIRECTION_TYPE_CHOICES, blank=True, null=True)
    
    # Document Information
    title_deed_number = models.CharField(max_length=50, blank=True, null=True)
    title_deed_date = models.DateField(blank=True, null=True)
    sale_deed_number = models.CharField(max_length=50)
    sale_deed_date = models.DateField()
    
    # Transaction Participants
    notary_name = models.CharField(max_length=255)
    witness1_name = models.CharField(max_length=255)
    witness2_name = models.CharField(max_length=255)
    guarantor_name = models.CharField(max_length=255, blank=True, null=True)
    
    # System Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_comment = models.TextField(blank=True, null=True)
    current_step = models.CharField(max_length=50, default='registration')
    documents = models.FileField(upload_to='land_documents/', validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])], blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_registration_type_display()} - {self.transaction_reference}"

    def clean(self):
        super().clean()
        if self.seller_national_id == self.buyer_national_id:
            raise ValidationError('Seller and buyer cannot have the same national ID.')
        # Only require sale_price for land sale
        if getattr(self, 'registration_type', 'sale') == 'sale' and not self.sale_price:
            raise ValidationError('Sale price is required for land sale transactions.')

class SurveyPayment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('verified', 'Verified'),
    ]
    
    PAYMENT_METHOD = [
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('mobile', 'Mobile Payment'),
    ]
    
    land_registration = models.OneToOneField(LandRegistration, on_delete=models.CASCADE)
    admin_name = models.CharField(max_length=255)
    payer_name = models.CharField(max_length=255)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    payment_date = models.DateField()
    payment_receipt = models.FileField(upload_to='payment_receipts/')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"Survey Payment - {self.payer_name}"

class LandSurvey(models.Model):
    land_registration = models.OneToOneField(LandRegistration, on_delete=models.CASCADE)
    survey_number = models.CharField(max_length=50, unique=True)
    parcel_number = models.CharField(max_length=50, unique=True)
    land_code = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=255)
    survey_date = models.DateField()
    surveyor_name = models.CharField(max_length=255)
    survey_location = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)
    survey_documents = models.FileField(upload_to='survey_documents/')
    land_direction = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"Land Survey - {self.survey_number}"

class TaxPayment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('verified', 'Verified'),
    ]
    
    land_registration = models.OneToOneField(LandRegistration, on_delete=models.CASCADE)
    admin_fullname = models.CharField(max_length=255)
    land_owner_name = models.CharField(max_length=255)
    land_reference_no = models.CharField(max_length=50)
    land_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    receipt_number = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"Tax Payment - {self.land_reference_no}"

class LandMapping(models.Model):
    MAPPING_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('verified', 'Verified'),
    ]
    
    land_registration = models.OneToOneField(LandRegistration, on_delete=models.CASCADE)
    land_reference = models.CharField(max_length=50)
    map_coordinates = models.CharField(max_length=255)
    mapping_date = models.DateField()
    mapped_by = models.CharField(max_length=255)
    mapping_status = models.CharField(max_length=20, choices=MAPPING_STATUS, default='pending')
    map_document = models.FileField(upload_to='map_documents/')
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"Land Mapping - {self.land_reference}"

class Approval(models.Model):
    APPROVAL_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned for Correction'),
    ]

    APPROVAL_LEVELS = [
        ('director_pending', 'Land Director Approval'),
        ('secretary_pending', 'Secretary Approval'),
        ('deputy_mayor_pending', 'Deputy Mayor Approval'),
        ('mayor_pending', 'Mayor Approval'),
        ('completed', 'Approval Process Completed'),
        ('rejected', 'Approval Process Rejected'),
    ]

    RETURN_STEPS = [
        ('registration', 'Land Registration'),
        ('survey_payment', 'Survey Payment'),
        ('land_survey', 'Land Survey'),
        ('tax_payment', 'Tax Payment'),
        ('land_mapping', 'Land Mapping'),
        ('certificate_generated', 'Certificate Generated'),
    ]

    land_registration = models.OneToOneField(LandRegistration, on_delete=models.CASCADE)
    current_approval_level = models.CharField(max_length=50, choices=APPROVAL_LEVELS, default='director_pending')
    return_step = models.CharField(max_length=50, choices=RETURN_STEPS, null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)
    rejection_date = models.DateTimeField(null=True, blank=True)
    returned_by = models.CharField(max_length=255, blank=True, null=True)

    # Land Director
    director_full_name = models.CharField(max_length=255, blank=True, null=True)
    director_title = models.CharField(max_length=100, blank=True, null=True)
    director_email = models.EmailField(blank=True, null=True)
    director_signature = models.FileField(upload_to='signatures/', blank=True, null=True)
    director_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    director_comment = models.TextField(blank=True, null=True)
    director_approval_date = models.DateField(null=True, blank=True)

    # Secretary
    secretary_full_name = models.CharField(max_length=255, blank=True, null=True)
    secretary_title = models.CharField(max_length=100, blank=True, null=True)
    secretary_email = models.EmailField(blank=True, null=True)
    secretary_signature = models.FileField(upload_to='signatures/', blank=True, null=True)
    secretary_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    secretary_comment = models.TextField(blank=True, null=True)
    secretary_approval_date = models.DateField(null=True, blank=True)

    # Deputy Mayor
    deputy_mayor_full_name = models.CharField(max_length=255, blank=True, null=True)
    deputy_mayor_title = models.CharField(max_length=100, blank=True, null=True)
    deputy_mayor_email = models.EmailField(blank=True, null=True)
    deputy_mayor_signature = models.FileField(upload_to='signatures/', blank=True, null=True)
    deputy_mayor_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    deputy_mayor_comment = models.TextField(blank=True, null=True)
    deputy_mayor_approval_date = models.DateField(null=True, blank=True)

    # Mayor
    mayor_full_name = models.CharField(max_length=255, blank=True, null=True)
    mayor_title = models.CharField(max_length=100, blank=True, null=True)
    mayor_email = models.EmailField(blank=True, null=True)
    mayor_signature = models.FileField(upload_to='signatures/', blank=True, null=True)
    mayor_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    mayor_comment = models.TextField(blank=True, null=True)
    mayor_approval_date = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"Approval Process - {self.land_registration.transaction_reference}"

class PasswordResetRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_resets')
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Password Reset for {self.user.username} ({self.status})"
    
    def has_pending_request(self):
        """Check if user has a pending request within 24 hours"""
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_time = timezone.now() - timedelta(hours=24)
        return PasswordResetRequest.objects.filter(
            user=self.user,
            status='pending',
            requested_at__gte=cutoff_time
        ).exists()
    
    @classmethod
    def get_pending_request(cls, user):
        """Get the most recent pending request for a user"""
        return cls.objects.filter(
            user=user,
            status='pending'
        ).order_by('-requested_at').first()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('password_reset', 'Password Reset Request'),
        ('registration', 'New Registration'),
        ('approval', 'Approval Required'),
        ('payment', 'Payment Received'),
        ('system', 'System Notification'),
    ]
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # For user-specific notifications
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    related_object_id = models.IntegerField(null=True, blank=True)  # For linking to specific objects
    related_object_type = models.CharField(max_length=50, null=True, blank=True)  # Model name
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type}: {self.title}"
