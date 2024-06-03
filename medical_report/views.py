from django.db.models.base import Model as Model
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,FormView,CreateView,View,UpdateView
from .forms import *
from django.urls import reverse_lazy,reverse
from django.contrib.auth.models import User
from .utils import password_reset_token
from django.core.mail import send_mail
from django.contrib.auth import login,logout,authenticate
from django.conf import settings
from .models import *

class PatientMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Patient.objects.filter(user = request.user).exists():
            pass
        else:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)
    
class HomePageView(PatientMixin,FormView):
    template_name = "medical/home.html"
    form_class = MedicalReportReaderForm
    success_url = '/'

    def form_valid(self, form):
        medical_report_data = form.get_file_data()
        self.request.session['output_data'] = medical_report_data
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        output_data = self.request.session.get('output_data')
        # for line in output_data:
        #     if line['min_value'] is not None and line['max_value'] is not None and line['current_value'] is not None:
        #         medical_rep = MedicalAnalysis.objects.create(
        #             patient=self.request.user,
        #             title=line['name'],
        #             min_val=line['min_value'],
        #             curr_val=line['current_value'],
        #             max_val=line['max_value'],
        #         )

        return context
    
class PatientRegisterView(CreateView):
    template_name = 'signup.html' 
    form_class = PatientRegisterForm
    success_url = reverse_lazy('medical:home')
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('full_name').split(' ')[0]
        last_name = form.cleaned_data.get('full_name').split(' ')[-1]
        print('first_name = ',first_name)
        print('last_name = ',last_name)
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            )
        form.instance.user = user
        login(self.request,user)
        return super().form_valid(form)

class PatientLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('medical:login')

class PatientLoginView(FormView):
    template_name = 'login.html'
    form_class = PatientLoginForm
    success_url =  reverse_lazy('medical:home')
    
    def form_valid(self, form):
        user_name = form.cleaned_data.get('username')
        user_pass = form.cleaned_data['password']
        usr = authenticate(username=user_name, password=user_pass)
        if usr is not None and Patient.objects.filter(user=usr).exists():
            login(self.request, usr)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)
    
    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        else:
            return self.success_url

class PatientProfileView(PatientMixin,TemplateView):
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context["patient"] = Patient.objects.get(user = current_user) 
        return context

class PatientUpdateView(PatientMixin,UpdateView):
    model = Patient
    form_class = PatientUpdateForm
    template_name = 'edit_profile.html'
    
    def get_object(self, *args, **kwargs):
        patient = get_object_or_404(Patient,pk=self.kwargs['pk'])
        return patient

    def get_success_url(self, *args, **kwargs):
       return reverse_lazy('medical:profile')

class PatientForgetPasswordView(FormView):
    template_name='forget_password.html'
    form_class = PatientForgetPasswordForm
    success_url = '/forget-password/?m=s'
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        url = self.request.META['HTTP_HOST']
        patient = Patient.objects.get(user__email = email)
        user = patient.user
        token = password_reset_token.make_token(user)
        message_content = f"""
                            Please go to the following url to able to reset your password, 
                            {url}/reset-password/{email}/{token}/
                           """
        send_mail(
            "Password Rest Link | Obour Medical Project",
            message_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently = False
        )
        return super().form_valid(form)
    
class PatientResetPasswordView(FormView):
    template_name='reset_password.html'
    form_class = PatientResetPasswordForm
    success_url = reverse_lazy('medical:login')
    
    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get('email')
        user = User.objects.get(email=email)
        token = self.kwargs.get('token')
        if user is not None and password_reset_token.check_token(user,token):
            pass
        else:
            return redirect(reverse('medical:forget_password') + '?m=e')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self,form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get('email')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)

class OurDoctorsView(TemplateView):
    template_name = 'medical/our_doctors.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_doctors"] = OurDoctors.objects.all()
        return context

class OurNewsView(TemplateView):
    template_name = 'medical/our_news.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_news"] = OurProjectNews.objects.all()
        # context["all_new_images"] = OurProjectNewsImages.objects.filter(new = lambda x:x.id)
        return context
