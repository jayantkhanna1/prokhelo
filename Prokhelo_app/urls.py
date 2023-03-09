from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Main Page Urls
    path('', views.MainMethods.index, name='index'),
    path('home', views.MainMethods.index, name='home'),
    path('user', views.MainMethods.user, name='user'),

    # Login Page Urls
    path('login', views.Login.login, name='login'),
    path('login_user', views.Login.login_user, name='login_user'),
    path('logout', views.Login.logout, name='logout'),

    # Signup Page Urls
    path('signup', views.Signup.signup, name='signup'),
    path('signup_user', views.Signup.signup_user, name='signup_user'),

    # OTP Page Urls
    path('otp_verify', views.Otp.otp_verify, name='otp_verify'),
    path('forgot_password', views.Otp.forgot_password, name='forgot_password'),
    path('forgot_password_form', views.Otp.forgot_password_form, name='forgot_password_form'),
    path('otp_verify_forgot_password', views.Otp.otp_verify_forgot_password, name='otp_verify_forgot_password'),
    path('reset_password', views.Otp.reset_password, name='reset_password'),

    # Onboarding Page Urls
    path('onboarding_form', views.Onboarding.onboarding_form, name='onboarding_form'),
    path('user_onboarding', views.Onboarding.user_onboarding, name='user_onboarding'),

    # Admin Page Urls
    path('admin_login',views.AdminMethods.admin_login,name="admin_login"),
    path('admin_login_form',views.AdminMethods.admin_login_form,name="admin_login_form"),
    path('admin_logout',views.AdminMethods.admin_logout,name="admin_logout"),
    path('admin_dashboard',views.AdminMethods.admin,name="admin"),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Adding static path


