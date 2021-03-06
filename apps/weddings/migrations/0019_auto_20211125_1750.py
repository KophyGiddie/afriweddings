# Generated by Django 3.2 on 2021-11-25 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weddings', '0018_auto_20211119_1646'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wallpost',
            options={'ordering': ('-created_at',), 'verbose_name_plural': 'Wall Post'},
        ),
        migrations.AddField(
            model_name='wedding',
            name='schedule',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='wallpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='WALLPOST/2021/11/25/17/50/55/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='couple_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/11/25/17/50/55/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='partner_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/11/25/17/50/55/'),
        ),
        migrations.AlterField(
            model_name='weddingmedia',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/25/17/50/55/'),
        ),
        migrations.AlterField(
            model_name='weddingteam',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/11/25/17/50/55/'),
        ),
    ]
