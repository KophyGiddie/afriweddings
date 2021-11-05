# Generated by Django 3.2 on 2021-11-04 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20211104_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='afuser',
            name='wedding_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='afuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/04/21/25/10/', verbose_name='Profile Pic'),
        ),
    ]
