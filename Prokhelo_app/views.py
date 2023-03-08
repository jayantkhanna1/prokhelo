from django.shortcuts import render, redirect
from .models import User, Admin
from passlib.hash import sha512_crypt as sha512
from django.contrib import messages
import string, random
from django.core.mail import send_mail
import os
from dotenv import load_dotenv
load_dotenv()

otp : int
class MainMethods:
    def index(request):
        # Checking if user is present in session
        if "PrivateTokenProkhelo" in request.session:
            return redirect('user')
        return render(request,'index.html')

    def user(request):
        if "PrivateTokenProkhelo" in request.session:
            # Getting user from database
            if User.objects.filter(private_token=request.session['PrivateTokenProkhelo']).exists():
                user = User.objects.get(private_token=request.session['PrivateTokenProkhelo'])
                username = user.username
                if username == None or username == "":
                    return redirect('onboarding_form')
                return render(request,'user.html',{'user': user})
        return redirect('login')
    
class Login:
    def login(request):
        return render(request,'login.html')
    
    def login_user(request):
        # Getting data from form
        email = request.POST.get('email')
        password = request.POST.get('password')
        password=sha512.hash(password, rounds=5000,salt="Prokhelo")

        # Checking if user exists
        if User.objects.filter(email=email,password=password).exists():
            user = User.objects.get(email=email,password=password)

            # If user exists then creating session and updating private token in database
            request.session['PrivateTokenProkhelo'] = ''.join(random.choices(string.ascii_lowercase +string.digits, k=30))
            user.private_token = request.session['PrivateTokenProkhelo']
            user.save()
            return redirect('user')

        # If user does not exists then redirecting to login page with error message
        else:
            messages.info(request, 'error')
            return redirect('login')
    
    def logout(request):
        # Deleting session so user is logged out
        del request.session['PrivateTokenProkhelo']
        return redirect('home')
    
class Signup:
    def signup(request):
        return render(request,'signup.html')
    
    def signup_user(request):
        # Getting data from form
        email = request.POST['email']
        password = request.POST['password']
        password=sha512.hash(password, rounds=5000,salt="Prokhelo")

        # Checking if user already exists if he/she does then redirecting to signup page with error message
        if User.objects.filter(email=email).exists():
            messages.info(request, 'error_already_exists')
            return redirect('signup')
        else:
            # If user does not exists then creating user and sending OTP via mail
            messages.info(request, 'success')
            global otp
            otp = ''.join(random.choices(string.ascii_lowercase +string.digits, k=6))
            message = "Your OTP is "+otp
            sender = os.getenv('EMAIL')
            reciever = [email]
            send_mail("OTP for Prokhelo",message,sender,recipient_list=reciever)
            return render(request,'otp.html',{'email': email,'password': password})

class Otp:
    def otp_verify(request):
        # Getting data from form
        email = request.POST['email']
        password = request.POST['password']
        otp_entered = request.POST['otp']
        global otp
        print(otp)
        print(otp_entered)
        # Checking if OTP entered by user is correct. If it is correct then creating session and updating private token in database
        if otp_entered == str(otp):
            res = ''.join(random.choices(string.ascii_lowercase +string.digits, k=30))
            request.session['PrivateTokenProkhelo'] = res
            user = User(private_token=res,email=email,password=password)
            user.save()
            return redirect('onboarding_form')
        
        # If OTP is incorrect then redirecting to signup page with error message
        else:
            messages.info(request, 'error')
            return render(request, 'otp.html',{'email': email,'password': password})

    def forgot_password(request):
        return render(request,'forgot_password.html')
    
    def forgot_password_form(request):
        email = request.POST['email']
        # Checking if user exists. If user exists then sending OTP via mail. else redirecting to forgot password page with error message
        if User.objects.filter(email=email).exists():
            global otp
            otp = ''.join(random.choices(string.ascii_lowercase +string.digits, k=6))
            message = "Your OTP is "+otp
            sender = os.getenv('EMAIL')
            reciever = [email]
            send_mail("OTP for Prokhelo",message,sender,recipient_list=reciever)
            messages.info(request, 'success')
            return render(request,'otp_verify_forgot_password.html',{'email': email})
        messages.info(request, 'error')
        return render(request,'forgot_password.html')
    
    def otp_verify_forgot_password(request):
        otp1 = request.POST['otp']
        email = request.POST['email']
        global otp
        if otp == str(otp1):
            return render(request,'change_password.html',{'email': email})
        messages.info(request, 'error')
        return render(request,'otp_verify_forgot_password.html')
    
    def reset_password(request):
        email = request.POST['email']
        password = request.POST['password']
        password=sha512.hash(password, rounds=5000,salt="Prokhelo")
        user = User.objects.get(email=email)
        user.password = password
        private_token = ''.join(random.choices(string.ascii_lowercase +string.digits, k=30))
        user.private_token = private_token
        request.session['PrivateTokenProkhelo'] = private_token
        user.save()
        return redirect('login')
    
class Onboarding:
    def onboarding_form(request):
        return render(request,'onboarding_form.html')
    
    def user_onboarding(request):
        username = request.POST['username']
        dob = request.POST['dob']
        userimage = request.FILES['userimage']
        if User.objects.filter(private_token=request.session['PrivateTokenProkhelo']).exists():
            user = User.objects.get(private_token=request.session['PrivateTokenProkhelo'])
            user.username = username
            user.dob = dob
            user.image = userimage
            user.save()
            return redirect('user')
        return redirect('login')
        
    
class AdminMethods:
    def admin_login(request):
        return render(request,'admin_login.html')
    
    def admin_login_form(request):
        # Getting data from form
        email = request.POST.get('email')
        password = request.POST.get('password')
        password=sha512.hash(password, rounds=5000,salt="Prokhelo")
        print(password)
        # Checking if user exists
        if Admin.objects.filter(email=email,password=password).exists():
            admin = Admin.objects.get(email=email,password=password)

            # If user exists then creating session and updating private token in database
            request.session['PrivateTokenProkheloAdmin'] = ''.join(random.choices(string.ascii_lowercase +string.digits, k=30))
            admin.private_token = request.session['PrivateTokenProkheloAdmin']
            admin.save()
            return redirect('admin')

        # If user does not exists then redirecting to login page with error message
        else:
            messages.info(request, 'error')
            return redirect('admin_login')
        
    def admin_logout(request):
        del request.session['PrivateTokenProkheloAdmin']
        return render(request,'admin_logout.html')
    
    def admin(request):
        if "PrivateTokenProkheloAdmin" in request.session:
            if Admin.objects.filter(private_token=request.session['PrivateTokenProkheloAdmin']).exists():
                users = User.objects.all()
                for user in users:
                    print(user.username)
                return render(request,'admin.html',{'users': users})
        return redirect('admin_login')