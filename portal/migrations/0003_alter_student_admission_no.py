# Generated by Django 4.2.3 on 2023-07-09 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_rename_recipt_no_studentinfo_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='admission_no',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
