# Generated by Django 3.2 on 2021-12-09 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weddings', '0024_auto_20211209_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='WALLPOST/2021/12/09/16/55/54w3qnkkccsSTgh1Nq/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='couple_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/12/09/16/55/54mMt26ngqQLTBCG4q/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='partner_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/12/09/16/55/54mMt26ngqQLTBCG4q/'),
        ),
        migrations.AlterField(
            model_name='weddingmedia',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/12/09/16/55/54mMt26ngqQLTBCG4q/'),
        ),
        migrations.AlterField(
            model_name='weddingteam',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2021/12/09/16/55/54mMt26ngqQLTBCG4q/'),
        ),
    ]
