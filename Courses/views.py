from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from Courses.models import *
# Create your views here.


def create_course_view(request):
    if request.method == 'POST':
        course_thumbnail = request.FILES.get('course_thumbnail', '')
        course_category = request.POST.get('course_category')
        course_title = request.POST.get('course_title')
        course_description = request.POST.get('course_description')

        if Course.objects.filter(course_title=course_title).exists():
            return JsonResponse({'status':'error', 'message':'Exact same Course Title already exists.'})
        course = Course.objects.create(created_by=request.user, course_thumbnail=course_thumbnail, course_category=course_category, course_title=course_title, course_description=course_description)
        messages.success(request, f'{course.course_title} Course created successfully.')
        return JsonResponse({'status':'success', 'success_url':f'/teacher/update/course/{course.id}/'})

    return render(request, 'courses/create_course.html')

def update_course_view(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        course_thumbnail = request.FILES.get('course_thumbnail', '')
        course_category = request.POST.get('course_category')
        course_title = request.POST.get('course_title')
        course_description = request.POST.get('course_description')

        courses_objs = Course.objects.filter(course_title=course_title)
        if courses_objs.exists():
            if course != courses_objs[0]:
                return JsonResponse({'status':'error', 'message':'Exact same Course Title already exists.'})

        course.course_thumbnail = course_thumbnail if course_thumbnail != '' else course.course_thumbnail
        course.course_category = course_category
        course.course_title = course_title
        course.course_description = course_description
        course.save()
        messages.success(request, f'Course Information updated successfully.')
        return JsonResponse({'status':'success', 'success_url':f'/teacher/update/course/{course.id}/'})

    return render(request, 'courses/update_course.html', context={'course':course})

def detail_course_view(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'courses/detail_course.html', context={'course':course})

def delete_course_view(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    messages.success(request, 'Course deleted successfully.')
    return redirect('list-courses-view')

def list_courses_view(request):
    courses = Course.objects.all()
    return render(request, 'courses/list_courses.html', context={'courses':courses})