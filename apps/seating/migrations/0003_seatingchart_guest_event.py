# Generated by Django 3.2 on 2021-11-25 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0007_auto_20211120_1526'),
        ('seating', '0002_auto_20211105_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='seatingchart',
            name='guest_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chart', to='guests.guestevent'),
        ),
    ]
