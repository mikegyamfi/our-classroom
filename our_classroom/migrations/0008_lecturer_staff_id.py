# Generated by Django 4.2.5 on 2023-09-11 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('our_classroom', '0007_lecturer_student_class_alter_course_day_taught'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='staff_id',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
