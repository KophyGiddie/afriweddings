# Generated by Django 3.2 on 2021-12-04 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rsvp', '0002_rsvp_guest_invitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='rsvpquestion',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rsvp_question', to=settings.AUTH_USER_MODEL),
        ),
    ]
