from django.contrib import admin

# Register your models here.
from revision.models import Course, AvailableTime, CourseSeen


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('item', 'name', 'seen', 'family', 'book', 'duration', 'started_learning')


@admin.register(AvailableTime)
class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('date', 'duration')


@admin.register(CourseSeen)
class CourseSeenAdmin(admin.ModelAdmin):
    list_display = ('date', 'course')
