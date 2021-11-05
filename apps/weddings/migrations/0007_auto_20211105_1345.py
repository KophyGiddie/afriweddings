# Generated by Django 3.2 on 2021-11-05 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weddings', '0006_auto_20211105_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='wedding',
            name='city',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='wallpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='WALLPOST/2021/11/05/13/45/13/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='country',
            field=models.CharField(blank=True, default='Ghana', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='currency',
            field=models.CharField(blank=True, default='GHS', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='partner_picture',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/05/13/45/13/'),
        ),
        migrations.AlterField(
            model_name='weddingmedia',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/05/13/45/13/'),
        ),
        migrations.AlterField(
            model_name='weddingteam',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/05/13/45/13/'),
        ),
    ]
