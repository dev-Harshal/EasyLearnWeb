import random
from django.utils import timezone
from django.contrib.auth import authenticate

def create_admin_profile(user,model):
    if user.role == 'Admin':
        while True:
            phone_number = input('Phone Number: ')
            if phone_number.isdigit() and len(phone_number) == 10:
                break
            else:
                print("Invalid phone number. Please enter a 10-digit number.")
        model.objects.create(user=user, phone_number=phone_number,
                            department='Admin', designation='Staff')

def login_user(request, role='Student'):
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    user = authenticate(email=email, password=password)
    if user is not None and user.role == role:
        otp_code = str(random.randint(1000,9999))
        request.session['otp_code'] = str(otp_code)
        request.session['otp_expiry'] = (timezone.now() + timezone.timedelta(seconds= 30)).timestamp()
        print('OTP CODE: ',otp_code) #Replace with send Email.
        return {'status':'success', 'message':'OTP Code send successfully to Email.'}
    else:
        return {'status':'error', 'message':'Invalid Email or Password.'}