# Generated by Django 5.1.6 on 2025-03-06 12:06

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
            name='CurriculumItem',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('item_type', models.CharField(choices=[('lesson', 'lesson'), ('quiz', 'quiz')], max_length=10)),
                ('item_order', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('course_thumbnail', models.ImageField(upload_to='CourseThumbnails/')),
                ('course_title', models.CharField(max_length=200)),
                ('course_category', models.CharField(max_length=100)),
                ('course_description', models.CharField(max_length=200)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'All Courses',
            },
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='curriculum', to='Courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('video_title', models.CharField(max_length=255)),
                ('video_file', models.FileField(upload_to='videos/')),
                ('note_file', models.FileField(blank=True, null=True, upload_to='notes/')),
                ('curriculum_item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lesson', to='Courses.curriculumitem')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quiz_question', models.CharField(max_length=255)),
                ('curriculum_item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='Courses.curriculumitem')),
            ],
        ),
        migrations.CreateModel(
            name='QuizOption',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('option', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='Courses.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('section_order', models.PositiveIntegerField(default=0)),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='Courses.curriculum')),
            ],
        ),
    ]
