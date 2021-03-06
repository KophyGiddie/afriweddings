# Generated by Django 3.2 on 2021-11-11 12:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weddings', '0010_auto_20211108_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='wedding',
            name='admin',
            field=models.ManyToManyField(blank=True, null=True, related_name='wedding_admins', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='wallpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='WALLPOST/2021/11/11/12/34/55/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='couple_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/11/11/12/34/55/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='partner_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/11/11/12/34/55/'),
        ),
        migrations.AlterField(
            model_name='weddingmedia',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/11/12/34/55/'),
        ),
        migrations.AlterField(
            model_name='weddingteam',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/11/12/34/55/'),
        ),
    ]
