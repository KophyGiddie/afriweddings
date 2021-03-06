# Generated by Django 3.2 on 2021-12-04 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weddings', '0022_auto_20211204_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='weddingscheduleevent',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='weddingscheduleevent',
            name='venue',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='wallpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='WALLPOST/2021/12/04/12/21/35/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='couple_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/12/04/12/21/35/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='partner_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/12/04/12/21/35/'),
        ),
        migrations.AlterField(
            model_name='weddingmedia',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/12/04/12/21/35/'),
        ),
        migrations.AlterField(
            model_name='weddingteam',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='PROFILE/2021/12/04/12/21/35/'),
        ),
    ]
