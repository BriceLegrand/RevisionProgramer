from collections import OrderedDict
from datetime import datetime
from django.shortcuts import render, render_to_response
import datetime as dt
# Create your views here.
from django.template import RequestContext

from revision.models import Course, FAMILIES
from revision.program_manager import ProgramManager


def planning(request):
    planning = OrderedDict()
    today = datetime.now().date()
    program_manager = ProgramManager()
    families = {}
    final_courses = []
    for family in FAMILIES:
        families[family[0]] = {}
        family_courses = list(Course.objects.filter(family=family[0]))
        final_courses.extend(family_courses)
        for course in family_courses:
            families[family[0]][course.id] = course

    targetDate = datetime.date(datetime(2019,3,18))

    while today <= targetDate:
        courses = program_manager.get_most_important_courses(today, families, simulate=True)
        planning[today] = courses
        today += dt.timedelta(days=1)

    nb_time_seen = {course: 0 for course in Course.objects.all()}
    for course_seen in program_manager.courses_seen:
        nb_time_seen[course_seen.course] += 1

    return render(request, 'planning.html', {"planning": planning, "final_courses": nb_time_seen})

def home(request):
    return render(request, 'home.html')

