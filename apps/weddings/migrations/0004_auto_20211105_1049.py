# Generated by Django 3.2 on 2021-11-05 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weddings', '0003_auto_20211105_0418'),
    ]

    operations = [
        migrations.AddField(
            model_name='wedding',
            name='checklist_completed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wedding',
            name='total_checklist',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='wallpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='WALLPOST/2021/11/05/10/49/00/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='partner_picture',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/05/10/49/00/'),
        ),
        migrations.AlterField(
            model_name='weddingmedia',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/05/10/49/00/'),
        ),
        migrations.AlterField(
            model_name='weddingteam',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/05/10/49/00/'),
        ),
    ]
