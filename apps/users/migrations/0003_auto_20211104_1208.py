# Generated by Django 3.2 on 2021-11-04 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_afuser_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='afuser',
            name='activation_token',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='afuser',
            name='email_initiation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='afuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/04/12/08/54/', verbose_name='Profile Pic'),
        ),
    ]
