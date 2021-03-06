# Generated by Django 3.2 on 2021-11-20 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0006_auto_20211119_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='has_confirmed',
        ),
        migrations.RemoveField(
            model_name='guestgroup',
            name='is_partner',
        ),
        migrations.RemoveField(
            model_name='guestgroup',
            name='is_wedding_creator',
        ),
        migrations.AddField(
            model_name='guestgroup',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='guestgroup',
            name='is_wedding_author',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='guestgroup',
            name='is_wedding_partner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='guestinvitation',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guests_invitations', to='guests.guestevent'),
        ),
    ]
