# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land_management', '0006_alter_approval_return_step_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='landregistration',
            name='registration_type',
            field=models.CharField(
                choices=[
                    ('sale', 'Land Sale'),
                    ('gift', 'Gift Land'),
                    ('inheritance', 'Inheritance'),
                    ('exchange', 'Land Exchange'),
                    ('donation', 'Donation'),
                    ('court_order', 'Court Order'),
                    ('government_allocation', 'Government Allocation'),
                ],
                default='sale',
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name='landregistration',
            name='sale_price',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=15,
                null=True,
            ),
        ),
    ]
