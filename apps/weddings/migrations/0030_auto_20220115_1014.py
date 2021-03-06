# Generated by Django 3.2 on 2022-01-15 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weddings', '0029_auto_20220110_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='WALLPOST/2022/01/15/10/14/136KNHpQwNTKkDBmKr/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='couple_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/01/15/10/14/13JH12C4LbCt6ssCHk/'),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='partner_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/01/15/10/14/13JH12C4LbCt6ssCHk/'),
        ),
        migrations.AlterField(
            model_name='weddingmedia',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/01/15/10/14/13JH12C4LbCt6ssCHk/'),
        ),
        migrations.AlterField(
            model_name='weddingteam',
            name='profile_picture',
            field=models.FileField(blank=True, null=True, upload_to='PROFILE/2022/01/15/10/14/13JH12C4LbCt6ssCHk/'),
        ),
        migrations.CreateModel(
            name='WeddingUserRole',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wedding_user_role', to=settings.AUTH_USER_MODEL)),
                ('wedding', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wedding_user_role', to='weddings.wedding')),
            ],
            options={
                'verbose_name_plural': 'Wedding User Roles',
                'ordering': ('id',),
            },
        ),
    ]
