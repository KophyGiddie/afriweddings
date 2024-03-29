# Generated by Django 3.2 on 2022-05-03 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weddings', '0034_auto_20220316_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='wedding',
            name='planner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='planner_wedding', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='wedding',
            name='planner_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='wallpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='WALLPOST/2022/05/03/12/42/43LvNMbbSHl74BBj1F/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='couple_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/05/03/12/42/43k3HmL7k3QTMQ1BtR/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='couple_picture_mobile',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/05/03/12/42/43k3HmL7k3QTMQ1BtR/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='partner_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/05/03/12/42/43k3HmL7k3QTMQ1BtR/'),
        ),
        migrations.AlterField(
            model_name='weddingmedia',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/05/03/12/42/43k3HmL7k3QTMQ1BtR/'),
        ),
        migrations.AlterField(
            model_name='weddingteam',
            name='profile_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/05/03/12/42/43k3HmL7k3QTMQ1BtR/'),
        ),
    ]
