# Generated by Django 4.2.4 on 2023-08-23 10:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userpanel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentwebsite',
            name='category',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contentwebsite',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contentwebsite',
            name='modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='contentwebsite',
            name='publish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contentwebsite',
            name='slug',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='contentwebsite',
            name='tags',
            field=models.CharField(blank=True, null=True),
        ),
    ]
