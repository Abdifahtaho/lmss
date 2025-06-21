from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class LandRegistration(models.Model):
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
    
    # Basic Information
    transaction_reference = models.CharField(max_length=20, unique=True)
    date_of_sale = models.DateField()
    register_date = models.DateField(auto_now_add=True)
    sale_price = models.DecimalField(max_digits=15, decimal_places=2)  # For SLS currency
    
    # Seller Information
    seller_full_name = models.CharField(max_length=255)
    seller_national_id = models.CharField(max_length=50)
    seller_birth_date = models.DateField()
    seller_phone = models.CharField(max_length=20)
    seller_address = models.TextField(blank=True, null=True)
    
    # Buyer Information
    buyer_full_name = models.CharField(max_length=255)
    buyer_national_id = models.CharField(max_length=50)
    buyer_phone = models.CharField(max_length=20)
    buyer_address = models.TextField(blank=True, null=True)
    
    # Land Information
    land_code = models.CharField(max_length=20, unique=True)
    land_size = models.CharField(max_length=10, choices=LAND_SIZE_CHOICES)
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
        return f"Land Registration - {self.transaction_reference}"

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
    survey_number = models.CharField(max_length=50)
    parcel_number = models.CharField(max_length=50)
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
