# Generated by Django 3.2 on 2021-11-08 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0002_invitation_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='first_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='invitation',
            name='last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
