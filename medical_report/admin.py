from django.contrib import admin
from .models import (
    Patient,
    MedicalAnalysis,
    MedicalAdvaices,
    OurDoctors,
    OurProjectNews,
    OurProjectNewsImages
)

admin.site.register(Patient)
admin.site.register(MedicalAnalysis)
admin.site.register(MedicalAdvaices)
admin.site.register(OurDoctors)
admin.site.register(OurProjectNews)
admin.site.register(OurProjectNewsImages)
