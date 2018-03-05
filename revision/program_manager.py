import random
from datetime import datetime
import datetime as dt
import math

from revision.models import Course, AvailableTime, FAMILIES, CourseSeen, DIFFICULTIES


class ProgramManager(object):
    def __init__(self):
        # FACILE  0 - 10 - 30 - 90 - 180 - 270 - 360 - 450
        # MOYEN   0 - 3 - 10 - 30 - 90 - 180 - 270 - 360 - 450
        # DIFFICILE 0 - 3 - 10 - 30 - 60 - 90 - 180 - 270 - 360 - 450
        self.diffs = [diff[0] for diff in DIFFICULTIES]
        self.intervals = {
            "EASY PEASY": [0, 7, 23, 30, 60, 60, 60, 60, 60, 60],
            "SO SO": [0, 3, 7, 20, 30, 60, 60, 60, 60, 60, 60],
            "DIFFICULT": [0, 3, 7, 20, 60, 60, 60, 60, 60, 60, 60,60],
            "REALLY DIFFICULT": [0, 3, 7, 20, 60, 60, 60, 60, 60, 60, 60, 60]
        }

        self.coeffs = [1, 2, 3, 5, 10, 15, 15, 15, 15, 15, 15]
        self.DURATION_DIMINUTION = 0.67
        self.courses_seen = list(CourseSeen.objects.all())
        self.courses_tracking = {}
        for course in Course.objects.all():
            seen = CourseSeen.objects.filter(course=course)
            if seen.count() != 0:
                last_seen = seen.order_by("-date")[0].date
                seen = seen.count()
            else:
                last_seen = datetime(1970, 1, 1).date()
                seen = 0
            self.courses_tracking[course.id] = {"last_seen": last_seen, "seen": seen}

    def is_it_ok_to_take_this_course(self, available_time, course):
        seen = self.courses_tracking[course.id]["seen"]
        course_duration = course.duration * math.pow(self.DURATION_DIMINUTION, min(seen + 1, 4))
        return available_time - course_duration >= dt.timedelta(0) or (
                available_time - course_duration > dt.timedelta(minutes=-30) and available_time > dt.timedelta(
            minutes=60))

    def get_most_important_courses(self, today_date, families, simulate=False):
        today = AvailableTime.objects.get(date=today_date)
        differences = self.compute_distance_to_due_date(families, today_date)
        ordered_diffs = sorted(differences.keys(), reverse=True)
        picked_courses = []

        available_time = today.duration
        for ordered_diff in ordered_diffs:
            late_courses = differences[ordered_diff]
            for late_course in late_courses:

                # if available_time.total_seconds() > 0:
                if self.is_it_ok_to_take_this_course(available_time, late_course):
                    available_time -= late_course.duration * math.pow(self.DURATION_DIMINUTION, min(self.courses_tracking[late_course.id]["seen"] + 1, 4))
                    picked_courses.append(late_course)
                    if simulate:
                        late_course.simulate_this_course_is_seen(today_date, self.courses_seen)
                        self.courses_tracking[late_course.id]["last_seen"] = today_date
                        self.courses_tracking[late_course.id]["seen"] += 1
        index_family = int(today_date.strftime("%Y%m%d")) % 6

        stopped_families = []
        sorted_families = {}
        indexes = {}
        for family in FAMILIES:
            indexes[family[0]] = 0
            sorted_families[family[0]] = sorted(families[family[0]].values(), key=lambda x: x.difficulty == "REALLY DIFFICULT",
                             reverse=True)
        while available_time.total_seconds() > 1800 and len(stopped_families) < 6:
            picked_family = FAMILIES[index_family % 6][0]
            if picked_family in stopped_families:
                index_family += 1
                continue
            try:
                courses = sorted_families[picked_family]
                course = courses[indexes[picked_family]]
                while self.courses_tracking[course.id]["seen"] != 0:
                    indexes[picked_family] += 1
                    course = courses[indexes[picked_family]]
                if available_time.total_seconds() > 0:
                # if self.is_it_ok_to_take_this_course(available_time, course):
                    picked_courses.append(course)
                    if simulate:
                        course.simulate_this_course_is_seen(today_date, self.courses_seen)
                        self.courses_tracking[course.id]["last_seen"] = today_date
                        self.courses_tracking[course.id]["seen"] += 1

                    available_time -= course.duration
            except IndexError as e:
                stopped_families.append(picked_family)
            index_family += 1
        return picked_courses


    def compute_distance_to_due_date(self, families, today):
        differences = {}
        for family in families.values():
            for course in family.values():
                if self.courses_tracking[course.id]["seen"] == 0:
                    continue

                coeff = self.coeffs[self.courses_tracking[course.id]["seen"]]
                interval = self.intervals[course.difficulty][self.courses_tracking[course.id]["seen"]]
                last_seen = self.courses_tracking[course.id]["last_seen"]
                diff = math.ceil(
                    (today -
                     last_seen -
                     dt.timedelta(days=interval)).total_seconds() / float(coeff))
                if diff >= 0:
                    if diff not in differences:
                        differences[diff] = [course]
                    else:
                        differences[diff].append(course)

        return differences

# def retrieve_course_info(self, courses_seen, course):
#     last_date = datetime(1970, 1, 1)
#     seen = 0
#     for course_seen in reversed(courses_seen):
#         if course_seen.course.id == course.id:
#             seen += 1
#             last_date = max(last_date, course_seen.date)
#     return last_date, seen
