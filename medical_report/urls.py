from django.urls import path
from .views import *

app_name = 'medical_report'

urlpatterns = [
  path('',HomePageView.as_view(),name='home'),  
  path('signup/',PatientRegisterView.as_view(),name='signup'),  
  path('logout/',PatientLogoutView.as_view(),name='logout'), 
  path('login/',PatientLoginView.as_view(),name='login'), 
  path('profile/',PatientProfileView.as_view(),name='profile'), 
  path('edit-profile/<int:pk>',PatientUpdateView.as_view(),name='edit_profile'), 
  path('forget-password/',PatientForgetPasswordView.as_view(),name='forget_password'), 
  path('reset-password/<email>/<token>/',PatientResetPasswordView.as_view(),name='reset_password'), 
  path('our-doctors/',OurDoctorsView.as_view(),name='our_doctors'), 
  path('our-news/',OurNewsView.as_view(),name='our_news'), 
]
