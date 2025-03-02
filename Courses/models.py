from django.db import models
from Users.models import *
# Create your models here.

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_thumbnail = models.ImageField(upload_to='CourseThumbnails/', null=False, blank=False)
    course_title = models.CharField(max_length=200, null=False, blank=False)
    course_category = models.CharField(max_length=100, null=False, blank=False)
    course_description = models.CharField(max_length=200, null=False, blank=False)
    created_by = models.ForeignKey(User, related_name='created_course', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.course_title
    
    class Meta:
        db_table = 'All Courses'

class Section(models.Model):
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'All Sections'
    
class Video(models.Model):
    section = models.ForeignKey(Section, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    note_file = models.FileField(upload_to='notes/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)  # Order field for sorting
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'All Videos'
        ordering = ['order']

class Quiz(models.Model):
    section = models.ForeignKey(Section, related_name='quizzes', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    order = models.PositiveIntegerField(default=0)  # Order field for sorting

    def __str__(self):
        return self.question

    class Meta:
        db_table = 'All Quizzes'
        ordering = ['order']