# Generated by Django 4.1.3 on 2024-08-20 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IssueApp', '0009_alter_teaminvitation_expires_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teaminvitation',
            name='expires_at',
        ),
    ]
