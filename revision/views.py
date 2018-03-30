import json
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
    events = []

    while today <= targetDate:
        courses = program_manager.get_most_important_courses(today, families, simulate=True)
        for course in courses:
            if course.is_last_seen_today(today):
                class_name = "seenToday"
            elif course.seen() == 0:
                class_name = "new"
            else:
                class_name = "revision"

            events.append({"start": str(today), "title": course.get_planning_text(),  "className": class_name})

        planning[today] = courses
        today += dt.timedelta(days=1)

    nb_time_seen = {course: 0 for course in Course.objects.all()}
    for course_seen in program_manager.courses_seen:
        nb_time_seen[course_seen.course] += 1
    return render(request, 'planning.html', {"final_courses": nb_time_seen, 'events': json.dumps(events)})

def home(request):
    return render(request, 'home.html')

