from django.urls import path, include
from rest_framework import routers

from .otp_views import (SendPhoneOTP, 
						ValidateOTP, 
						Register,
						PasswordForgot,
						ValidatePassForgotOTP,
						ForgotChangePassword,
						ReffView)

from knox import views as knox_views
from . import views



app_name = 'account'
router = routers.DefaultRouter()
router.register(r'user', views.UserView, basename='user')


urlpatterns = [
	path('referred_by/', ReffView.as_view(), name= 'ref'),
	
	path('sendotp/', SendPhoneOTP.as_view(), name= 'sendotp'),
	path('validateotp/', ValidateOTP.as_view(), name='validateotp'),
	path('register/', Register.as_view(), name= 'register'),

  	path('login/', views.LoginView.as_view(), name='login'),
 	path('logout/', knox_views.LogoutView.as_view(), name='logout'),

	#url : http://127.0.0.1:8000/users-api/user/3/changephoneotp/ THIS IS THE API FOR SENDING OTP TO CHANGE PHONE
	path('', include(router.urls)),

  	path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),

 	path('send_forgot_password_otp/', PasswordForgot.as_view(), name='sendforgototp'),
	path('validate_forgot_password_otp/', ValidatePassForgotOTP.as_view(), name='validateforgototp'),
	path('change_forgot_password/', ForgotChangePassword.as_view(), name='changeforgot')


]