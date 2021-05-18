# Generated by Django 3.2.2 on 2021-05-18 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_apirequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apirequest',
            name='host',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='apirequest',
            name='method',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='apirequest',
            name='path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='apirequest',
            name='requester_ip',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='apirequest',
            name='user_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
