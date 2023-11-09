from django.contrib import admin
from tutors.models import TutorProfile, PriceList

# Register your models here.
admin.site.register(TutorProfile)

admin.site.register(PriceList)
