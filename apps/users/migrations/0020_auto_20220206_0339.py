# Generated by Django 3.2 on 2022-02-06 03:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20220204_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='wedding_id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
        migrations.AlterField(
            model_name='afuser',
            name='profile_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/02/06/03/39/01bH7D2sQBKCpGMt0R/', verbose_name='Profile Pic'),
        ),
    ]
