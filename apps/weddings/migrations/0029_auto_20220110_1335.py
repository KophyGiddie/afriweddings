# Generated by Django 3.2 on 2022-01-10 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weddings', '0028_auto_20211223_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='WALLPOST/2022/01/10/13/35/33ppvR8gGgqMGC21q9/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='couple_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/01/10/13/35/33mBqvGSN226q9P7mm/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partner_wedding', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='partner_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/01/10/13/35/33mBqvGSN226q9P7mm/'),
        ),
        migrations.AlterField(
            model_name='weddingmedia',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/01/10/13/35/33mBqvGSN226q9P7mm/'),
        ),
        migrations.AlterField(
            model_name='weddingteam',
            name='profile_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/01/10/13/35/33mBqvGSN226q9P7mm/'),
        ),
    ]
