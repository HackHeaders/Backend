# Generated by Django 4.2.16 on 2024-10-20 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carrier', '0015_payment_date_expiration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16, unique=True)),
                ('expiration_date', models.DateField()),
                ('cvv', models.CharField(max_length=3)),
                ('holder_name', models.CharField(max_length=255)),
                ('holder_cpf', models.CharField(max_length=11)),
                ('installments', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
