from django.db import models
from Users.models import *
# Create your models here.

class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    course_thumbnail = models.ImageField(upload_to='CourseThumbnails/', null=False, blank=False)
    course_title = models.CharField(max_length=200, null=False, blank=False)
    course_category = models.CharField(max_length=100, null=False, blank=False)
    course_description = models.CharField(max_length=200, null=False, blank=False)
    created_by = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.course_title
    
    class Meta:
        db_table = 'All Courses'


class Curriculum(models.Model):
    id = models.BigAutoField(primary_key=True)
    course = models.OneToOneField(Course, related_name='curriculum' ,on_delete=models.CASCADE)
    
class Section(models.Model):
    id = models.BigAutoField(primary_key=True)
    curriculum = models.ForeignKey(Curriculum, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    section_order = models.PositiveIntegerField(null=False, blank=False, default=0)

class CurriculumItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    section = models.ForeignKey(Section, related_name='items', on_delete=models.CASCADE)
    item_type = models.CharField(max_length=10, null=False, blank=False, choices=(('lesson','lesson'), ('quiz','quiz')))
    item_order = models.PositiveIntegerField(null=False, blank=False, default=0)

class Lesson(models.Model):
    id = models.BigAutoField(primary_key=True)
    curriculum_item = models.OneToOneField(CurriculumItem, related_name='lesson', on_delete=models.CASCADE)
    video_title = models.CharField(max_length=255, null=False, blank=False)
    video_file = models.FileField(upload_to='videos/')
    note_file = models.FileField(upload_to='notes/', blank=True, null=True)

class Quiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    curriculum_item = models.OneToOneField(CurriculumItem, related_name='quiz', on_delete=models.CASCADE)
    quiz_question = models.CharField(max_length=255, null=False, blank=False)

class QuizOption(models.Model):
    id = models.BigAutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, related_name='options', on_delete=models.CASCADE)
    option = models.CharField(max_length=255, null=False, blank=False)
    is_correct = models.BooleanField(default=False)







