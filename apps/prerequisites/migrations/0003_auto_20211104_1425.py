# Generated by Django 3.2 on 2021-11-04 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prerequisites', '0002_country'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='defaultchecklistcategory',
            options={'ordering': ('name',), 'verbose_name_plural': 'Default Checklist Category'},
        ),
        migrations.RenameField(
            model_name='defaultchecklistcategory',
            old_name='title',
            new_name='identifier',
        ),
        migrations.AddField(
            model_name='country',
            name='identifier',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='defaultchecklist',
            name='identifier',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='defaultchecklistcategory',
            name='name',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='defaultchecklistschedule',
            name='identifier',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
