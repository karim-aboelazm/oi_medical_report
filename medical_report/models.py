from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User,
                                verbose_name=('Patient User'),
                                on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name=('Patient Full Name'),
                                 max_length=200)
    address = models.CharField(verbose_name=('Patient Address'),
                               max_length=200)
    image = models.ImageField(verbose_name=('Patient Image'),
                              upload_to='Patient/Images/')
    phone = models.CharField(verbose_name=('Patient Phone'),
                             max_length=15,
                             unique=True)
    class Meta:
        verbose_name_plural = 'Patient'
    
    def __str__(self):
        return self.full_name
    
class MedicalAnalysis(models.Model):
    patient = models.ForeignKey(Patient,
                             verbose_name=('Analysis User'),
                             on_delete=models.CASCADE)
    title = models.CharField(verbose_name=('Analysis Title'),
                             max_length=200)
    min_val = models.CharField(verbose_name=('Analysis Minimum Value'),
                               max_length=5)
    curr_val = models.CharField(verbose_name=('Analysis Current Value'),
                               max_length=5)
    max_val = models.CharField(verbose_name=('Analysis Maximum Value'),
                               max_length=5)
    class Meta:
        verbose_name_plural = 'Medical Analysis'
    
    def __str__(self):
        return f"Analysis ({self.title} - {self.curr_val}) for patient {self.patient.full_name}"
    
class MedicalAdvaices(models.Model):
    analysis = models.ForeignKey(MedicalAnalysis,
                                 verbose_name=('Medical Analysis'),
                                 on_delete=models.CASCADE)
    advice = models.TextField(verbose_name=('Medical Advice'))
    
    class Meta:
        verbose_name_plural = 'Medical Advaices'
    
    def __str__(self):
        return f"Advise for analysis {self.analysis.title}"

class OurDoctors(models.Model):
    doctor_name = models.CharField(verbose_name="Doctor Name",max_length=200)
    doctor_major = models.CharField(verbose_name="Doctor Major",max_length=200)
    doctor_image = models.ImageField(verbose_name="Doctor Image",upload_to="doctor/images")
    doctor_phone = models.CharField(verbose_name="Doctor Phone",max_length=200)
    doctor_email = models.CharField(verbose_name="Doctor Email",max_length=200,null=True,blank=True)
    doctor_whatsapp = models.CharField(verbose_name="Doctor Whatsapp",max_length=200,null=True,blank=True)
    doctor_fb_url = models.URLField(verbose_name="Doctor Facebook",null=True,blank=True)
    def __str__(self):
        return self.doctor_name

class OurProjectNews(models.Model):
    title = models.CharField(verbose_name="News Title",max_length=200)
    description = models.TextField(verbose_name="News Description")
    def __str__(self):
        return self.title

class OurProjectNewsImages(models.Model):
    new = models.ForeignKey(OurProjectNews,on_delete=models.CASCADE)
    image =  models.ImageField(verbose_name="News Image",upload_to="news/images")
    def __str__(self):
        return self.new.title + f"Image [{self.new.id} - {self.id}]"

