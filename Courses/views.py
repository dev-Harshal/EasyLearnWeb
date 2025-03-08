from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
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
    if request.method == 'POST':

        try:
            print(request.POST,"DATA")
            # Get the course
            course = get_object_or_404(Course, id=course_id)

            # Create or get the curriculum for the course
            curriculum, created = Curriculum.objects.get_or_create(course=course)

            # Clear previous sections and items if necessary (optional, based on your need)
            curriculum.sections.all().delete()

            # Iterate over sections and save them
            section_titles = request.POST.getlist('section_title[]')
            section_orders = request.POST.getlist('section_order[]')

            for section_idx, (section_title, section_order) in enumerate(zip(section_titles, section_orders)):

                section = Section.objects.create(
                    curriculum = curriculum,
                    title = section_title,
                    section_order = int(section_order)
                )

                print(f'({section.section_order})', section_title)

                item_types = request.POST.getlist(f'sections[{section_order}][items][type][]')
                item_orders = request.POST.getlist(f'sections[{section_order}][items][order][]')
                print('ITEMS: ',item_types,item_orders)

                for item_idx, (item_type, item_order) in enumerate(zip(item_types, item_orders)):
                    
                    curriculum_item = CurriculumItem.objects.create(
                        section = section,
                        item_type = item_type,
                        item_order = int(item_order)
                    )
                    
                    # Handle lessons (videos)
                    if item_type == 'lesson':
                        video_title = request.POST.get(f'sections[{section.section_order}][items][{item_order}][title][]')
                        video_file = request.FILES.get(f'sections[{section.section_order}][items][{item_order}][video_file][]')
                        if not video_file:
                            video_file = request.POST.get(f'sections[{section.section_order}][items][{item_order}][video_file_existing]')
                        note_file = request.FILES.get(f'sections[{section.section_order}][items][{item_order}][note_file][]', None)
                        if not note_file:
                            note_file = request.POST.get(f'sections[{section.section_order}][items][{item_order}][note_file_existing]')

                        lesson = Lesson.objects.create(
                            curriculum_item = curriculum_item,
                            video_title = video_title,
                            video_file = video_file,
                            note_file = note_file
                        )

                    # Handle quizzes
                    else:
                        quiz_question = request.POST.get(f'sections[{section.section_order}][items][{item_order}][question][]')
                        
                        quiz = Quiz.objects.create(
                            curriculum_item = curriculum_item,
                            quiz_question = quiz_question
                        )

                            # Handle quiz options (assumes 4 options)
                        for option_number in range(1, 5):
                            option_text = request.POST.get(f'sections[{section.section_order}][items][{item_order}][options][{option_number}][text][]')
                            is_correct = request.POST.get(f'sections[{section.section_order}][items][{item_order}][is_correct][]') == str(option_number)   
                            
                            quiz_option = QuizOption.objects.create(
                                quiz = quiz,
                                option = option_text,
                                is_correct = is_correct
                            )


            messages.success(request, 'Video and Quizz added.')
            return JsonResponse({'status': 'success', 'success_url': f'/teacher/detail/course/{course_id}/'}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

