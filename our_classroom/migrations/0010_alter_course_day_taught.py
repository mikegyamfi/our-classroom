# Generated by Django 4.2.5 on 2023-09-25 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('our_classroom', '0009_information_student_class_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='day_taught',
            field=models.CharField(blank=True, choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], max_length=200, null=True),
        ),
    ]
