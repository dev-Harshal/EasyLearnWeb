from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from Users.models import User, Profile
from Users.services import *

def index_view(request):
    return render(request, 'users/index.html')

# --- AUTHENTICATION VIEWS ---

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        institute = request.POST.get('institute')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'status':'error', 'message':'Email address already exists.'})
        if password != confirm_password:
            return JsonResponse({'status':'error', 'message':'Passwords does not match.'})

        user = User.objects.create_user(
            first_name = first_name.title(),
            last_name = last_name.title(),
            institute = institute,
            email = email.lower(),
            password = password, 
            role='Student'
        )
        messages.success(request, f'{user.first_name} {user.last_name} registered successfully.')
        return JsonResponse({'status':'success', 'success_url':'/login/'})
    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        response = login_user(request)
        return JsonResponse(response)
    return render(request, 'users/login.html')

def staff_login_view(request, role):
    if request.method == 'POST':
        response = login_user(request, role=role.title())
        return JsonResponse(response)
    return render(request, 'users/staff_login.html', context={'role':role.title()})

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        otp_code = request.POST.get('otp_code')
        otp_expiry = request.session.get('otp_expiry', 0)

        if timezone.now().timestamp() > otp_expiry:
            return JsonResponse({'status':'error', 'message':'OTP Code expired.Try again.'})
        if str(otp_code) == request.session.get('otp_code'):
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'{user.first_name} {user.last_name[0]} logged in successfully.')
                success_url = '/' if user.role == 'Student' else f'/{user.role.lower()}/'
                return JsonResponse({'status':'success', 'success_url':success_url})
        return JsonResponse({'status':'error', 'message':'OTP Code invalid.Try again.'})

def logout_view(request):
    user = request.user
    logout(request)
    messages.success(request, f'{user.first_name} {user.last_name[0]} logged out successfully.')
    return redirect('index-view')

# ADMIN VIEWS

def admin_index_view(request):
    return render(request, 'users/admin/admin_index.html')

def admin_create_teacher_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        profile_photo = request.FILES.get('profile_photo', '')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'status':'error', 'message':'Email address already exists.'})
        if Profile.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'status':'error', 'message':'Phone Number already exists.'})
        if password != confirm_password:
            return JsonResponse({'status':'error', 'message':'Passwords does not match.Try again.'})
        
        user = User.objects.create_user(profile_photo=profile_photo, first_name=first_name.title(), last_name=last_name.title(),
                                        email=email.lower(), password=password, role='Teacher')
        Profile.objects.create(user=user, phone_number=phone_number, designation=designation, department=department)
        
        messages.success(request, f'{user.first_name} {user.last_name[0]} created successfully.')
        success_url = f'/admin/update/teacher/{user.id}'
        return JsonResponse({'status':'success','success_url':success_url})
    return render(request, 'users/admin/create_teacher.html')

def admin_update_teacher_view(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        profile_photo = request.FILES.get('profile_photo', '')

        if User.objects.filter(email=email).exists():
            if email != user.email:
                return JsonResponse({'status':'error', 'message':'Email address already exists.'})
        if Profile.objects.filter(phone_number=phone_number).exists():
            if phone_number != user.profile.phone_number:
                return JsonResponse({'status':'error', 'message':'Phone Number already exists.'})

        profile = Profile.objects.get(user=user)
        user.first_name = first_name.title() if first_name != '' else user.first_name
        user.last_name = last_name.title() if last_name != '' else user.last_name
        user.email = email.lower() if email != '' else user.email
        user.profile_photo = profile_photo if profile_photo != '' else user.profile_photo
        profile.phone_number = phone_number if phone_number != '' else profile.phone_number
        profile.designation = designation if designation != '' else profile.designation
        profile.department = department if department != '' else profile.department
        user.save()
        profile.save()
        messages.success(request, f'{user.first_name} {user.last_name[0]} profile updated successfully.')
        return JsonResponse({'status':'success', 'success_url':f'/admin/update/teacher/{user.id}/'})
    return render(request, 'users/admin/update_teacher.html', context={'user':user})

def admin_list_user_view(request, role):
    users = User.objects.filter(role=role.title())
    return render(request, 'users/admin/list_user.html', context={'role':role.title(), 'users':users})

# TEACHER VIEWS

def teacher_index_view(request):
    return render(request, 'users/teacher/teacher_index.html')

def teacher_list_student_view(request):
    users = User.objects.filter(role='Student')
    return render(request, 'users/teacher/list_student.html', context={'users':users})

# ADMIN AND TEACHER COMMON

def delete_user_view(request, id):
    user = User.objects.get(id=id)
    user_fullname = f'{user.first_name} {user.last_name[0]}'
    user.delete()
    messages.success(request, f'{user_fullname} deleted successfully.')
    return redirect(request.META.get('HTTP_REFERER', f'/{request.user.role.lower()}/'))

def staff_profile_view(request, role):
    if request.method == 'POST':
        id = request.POST.get('id')
        profile_photo = request.FILES.get('profile_photo', '')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        if User.objects.filter(email=email).exists():
            if email != request.user.email:
                return JsonResponse({'status':'error', 'message':'Email address already exists.'})
        if Profile.objects.filter(phone_number=phone_number).exists():
            if phone_number != request.user.profile.phone_number:
                return JsonResponse({'status':'error', 'message':'Phone Number already exists.'})

        user = User.objects.get(id=id)
        profile = Profile.objects.get(user=user)
        user.first_name = first_name.title()
        user.last_name = last_name.title()
        user.email = email.lower()
        user.profile_photo = profile_photo if profile_photo != '' else user.profile_photo
        profile.phone_number = phone_number
        user.save()
        profile.save()
        messages.success(request, f'{user.first_name} {user.last_name[0]} profile saved successfully.')
        return JsonResponse({'status':'success', 'success_url':f'/{user.role.lower()}/profile/'})
    return render(request, 'users/staff_profile.html',context={'role':role})

def change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        email = request.user.email

        user = authenticate(email=email, password=current_password)
        if user is not None:
            if new_password != confirm_password:
                return JsonResponse({'status':'error', 'message':'Passwords does not match.'})
            user.set_password(new_password)
            user.save()
            login(request,user)
            messages.success(request, 'Password updated successfully.')
            return JsonResponse({'status':'success', 'success_url':f'/{user.role.lower()}/profile/'})
        else:
            return JsonResponse({'status':'error', 'message':'Current Password does not match.'})
    else:
        return HttpResponseBadRequest("BAD REQUEST(400):GET NOT ALLOWED")