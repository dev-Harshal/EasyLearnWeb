# Generated by Django 5.1.6 on 2025-02-26 18:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_thumbnail', models.ImageField(upload_to='CourseThumbnails/')),
                ('course_title', models.CharField(max_length=200)),
                ('course_category', models.CharField(max_length=100)),
                ('course_description', models.CharField(max_length=200)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_course', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'All Courses',
            },
        ),
    ]
