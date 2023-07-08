# Generated by Django 4.2.3 on 2023-07-08 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('recipt_no', models.CharField(max_length=20, unique=True)),
                ('department', models.CharField(max_length=50)),
                ('student_number', models.CharField(max_length=20)),
                ('parent_name', models.CharField(max_length=50)),
                ('parent_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('original', models.BooleanField()),
                ('photocopy', models.BooleanField()),
                ('count', models.IntegerField()),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.document')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.student')),
            ],
        ),
    ]