# Generated by Django 3.2 on 2021-11-19 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weddings', '0017_auto_20211119_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='wedding',
            name='pending_guests',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='wallpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='WALLPOST/2021/11/19/16/46/43/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='couple_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/11/19/16/46/43/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='partner_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/11/19/16/46/43/'),
        ),
        migrations.AlterField(
            model_name='weddingmedia',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/19/16/46/43/'),
        ),
        migrations.AlterField(
            model_name='weddingteam',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/19/16/46/43/'),
        ),
    ]
