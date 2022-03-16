# Generated by Django 3.2 on 2022-03-16 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weddings', '0032_auto_20220218_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='wedding',
            name='couple_picture_mobile',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/03/16/14/36/24nLDddDSLBPbC27jN/'),
        ),
        migrations.AlterField(
            model_name='wallpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='WALLPOST/2022/03/16/14/36/24GLfKGbklckB4KnhK/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='couple_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/03/16/14/36/24nLDddDSLBPbC27jN/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='partner_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/03/16/14/36/24nLDddDSLBPbC27jN/'),
        ),
        migrations.AlterField(
            model_name='weddingmedia',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/03/16/14/36/24nLDddDSLBPbC27jN/'),
        ),
        migrations.AlterField(
            model_name='weddingteam',
            name='profile_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/03/16/14/36/24nLDddDSLBPbC27jN/'),
        ),
    ]
