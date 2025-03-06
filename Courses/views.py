from django.http import HttpResponse, JsonResponse
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
            return JsonResponse({'status':'error', 'message':'Same Title already exists.'})
        course = Course.objects.create(created_by=request.user, course_thumbnail=course_thumbnail, course_category=course_category, course_title=course_title, course_description=course_description)
        messages.success(request, f'Course of {course_category} created successfully.')
        return JsonResponse({'status':'success', 'success_url':f'/teacher/detail/course/{course.id}/'})

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
                return JsonResponse({'status':'error', 'message':'Same Title already exists.'})

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
    courses = request.user.courses.all()
    return render(request, 'courses/list_courses.html', context={'courses':courses})

def save_curriculum_view(request, course_id):

    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        sections = request.POST.getlist('section[]')

        for i, section_title in enumerate(sections, start=1):

            section = Section.objects.create(course=course, title=section_title)

            video_titles = request.POST.getlist(f'video_title[{i}][]')
            video_files = request.FILES.getlist(f'video_file[{i}][]')
            note_files = request.FILES.getlist(f'note_file[{i}][]')
            
            for j, video_title in enumerate(video_titles):
                video_file = video_files[j] if j < len(video_files) else None
                note_file = note_files[j] if j < len(note_files) else None

                Video.objects.create(
                    section=section,
                    title=video_title,
                    video_file=video_file,
                    note_file=note_file,
                    order=j
                )
                
            quiz_questions = request.POST.getlist(f'quiz_question[{i}][]')
            quiz_option_as = request.POST.getlist(f'quiz_option_a[{i}][]')
            quiz_option_bs = request.POST.getlist(f'quiz_option_b[{i}][]')
            quiz_option_cs = request.POST.getlist(f'quiz_option_c[{i}][]')
            quiz_option_ds = request.POST.getlist(f'quiz_option_d[{i}][]')
            correct_answers = request.POST.getlist(f'isCorrect[{i}][]')
            
            for k, question in enumerate(quiz_questions):
                Quiz.objects.create(
                    section=section,
                    question=question,
                    option_a=quiz_option_as[k],
                    option_b=quiz_option_bs[k],
                    option_c=quiz_option_cs[k],
                    option_d=quiz_option_ds[k],
                    correct_answer=correct_answers[k],
                    order=k
                )




        return JsonResponse({'status':'success'})