# Generated by Django 4.2.16 on 2024-09-05 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authUser', '0004_offices_employe_dataemploye'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employe',
            name='office',
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
