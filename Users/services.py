from django.utils import timezone
import random
from django.contrib.auth import authenticate

def login_user(request,role='Student'):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(email=email, password=password)
    if user is not None and user.role == role:
        otp_code = str(random.randint(1000,9999))
        request.session['otp_code'] = str(otp_code)
        request.session['otp_expiry'] = (timezone.now() + timezone.timedelta(seconds= 30)).timestamp()
        print('OTP CODE: ',otp_code)
        return {'status':'success', 'message':'OTP Code send successfully to Email.'}
    else:
        return {'status':'error', 'message':'Invalid Email or Password.'}