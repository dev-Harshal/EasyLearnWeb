from django.db import models
from Users.models import *
# Create your models here.

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_thumbnail = models.ImageField(upload_to='CourseThumbnails/', null=False, blank=False)
    course_title = models.CharField(max_length=200, null=False, blank=False)
    course_category = models.CharField(max_length=100, null=False, blank=False)
    course_description = models.CharField(max_length=200, null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.course_title
    
    class Meta:
        db_table = 'Courses Table'
