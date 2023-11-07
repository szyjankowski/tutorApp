from django.contrib import admin
from tutors.models import TutorProfile, Subject, PriceList

# Register your models here.
admin.site.register(TutorProfile)

admin.site.register(Subject)

admin.site.register(PriceList)
