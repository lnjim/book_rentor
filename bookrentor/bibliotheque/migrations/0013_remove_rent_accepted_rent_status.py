# Generated by Django 4.1.4 on 2023-01-07 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibliotheque', '0012_library_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rent',
            name='accepted',
        ),
        migrations.AddField(
            model_name='rent',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10),
        ),
    ]
