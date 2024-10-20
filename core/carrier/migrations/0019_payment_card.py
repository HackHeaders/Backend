# Generated by Django 4.2.16 on 2024-10-20 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carrier', '0018_alter_card_expiration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='carrier.card'),
        ),
    ]
