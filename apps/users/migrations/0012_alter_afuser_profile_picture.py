# Generated by Django 3.2 on 2021-11-25 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_afuser_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afuser',
            name='profile_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/11/25/17/50/55/', verbose_name='Profile Pic'),
        ),
    ]
