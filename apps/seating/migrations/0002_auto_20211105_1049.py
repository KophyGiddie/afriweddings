# Generated by Django 3.2 on 2021-11-05 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0001_initial'),
        ('seating', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seatingchart',
            name='guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chart', to='guests.guest'),
        ),
        migrations.AlterField(
            model_name='seatingchart',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chart', to='seating.seatingtable'),
        ),
    ]