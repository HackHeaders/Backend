# Generated by Django 4.2.16 on 2024-10-19 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrier', '0011_alter_payment_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payment_method',
            new_name='payment_method_id',
        ),
    ]
