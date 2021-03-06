# Generated by Django 3.2 on 2021-11-04 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weddings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('invitation_code', models.CharField(blank=True, max_length=200, null=True)),
                ('invitation_type', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, default='PENDING', max_length=200)),
                ('email_sent', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('invited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invitation', to=settings.AUTH_USER_MODEL)),
                ('invitee_role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invitation', to='weddings.weddingrole')),
                ('wedding', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invitation', to='weddings.wedding')),
            ],
            options={
                'verbose_name_plural': 'Invitation',
                'ordering': ('-created_at',),
            },
        ),
    ]
