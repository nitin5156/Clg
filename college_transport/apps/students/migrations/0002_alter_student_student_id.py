# Generated by Django 5.1.6 on 2025-02-23 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(default='A4F526B388', max_length=20, unique=True),
        ),
    ]
