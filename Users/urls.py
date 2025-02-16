from django.urls import path
from Users.views import *

urlpatterns = [
    path('', index_view, name='index-view'),    
    path('register/', register_view, name='register-view'),
    path('login/', login_view, name='login-view'),    
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('logout/', logout_view, name='logout-view'),

    path('<str:role>/login/', staff_login_view, name='staff-login-view'),
    path('<str:role>/profile/', profile_view, name='profile-view'),
    path('change-password/', change_password_view, name='changepassword-view'),
    path('delete/<int:id>/', delete_user_view, name='delete-user-view'),

    path('admin/', admin_index_view, name='admin-index-view'),
    path('admin/create/teacher/', admin_create_teacher_view, name='admin-create-teacher-view'),
    path('admin/update/teacher/<int:id>/', admin_update_teacher_view, name='admin-update-teacher-view'),
    path('admin/list/<str:role>/', admin_list_user_view, name='admin-list-user-view'),
    

    path('teacher/', teacher_index_view, name='teacher-index-view'),
    path('teacher/list/<str:role>/', teacher_list_user_view, name='teacher-list-user-view'),
    
]
