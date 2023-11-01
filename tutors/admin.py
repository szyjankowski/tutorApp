from django.contrib import admin
from tutors.models import TutorProfile, Subject, PriceList


# Register your models here.
@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ("tutor", "description_tutor")
    search_fields = ("tutor__email",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ("tutor", "subject", "hour_price")
    search_fields = ("tutor__tutor__email", "subject__name")
