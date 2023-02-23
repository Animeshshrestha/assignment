# Generated by Django 4.1.7 on 2023-02-22 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('faculty_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_of_birth', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
