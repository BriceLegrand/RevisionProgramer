import django
from django.db import models
from django.db.models import CASCADE
from django.utils import timezone
from datetime import date, timedelta, datetime

FAMILIES = (
    ("CHIRURGIE_ORALE", 'Chirurgie orale'),
    ("PROTHESE", 'Prothèse'),
    ("ORTHODONTIE", 'Orthodontie'),
    ("PARODONTOLOGIE", 'Parodontologie'),
    ("PEDODONTIE", 'Pedodontie'),
    ("OCE", 'OCE'),
)

BOOKS = (("CHIR_PARO", "CHIR_PARO"), ("PEDO_ORTHO", "PEDO_ORTHO"), ("OCE_PROTHESE", "OCE_PROTHESE"))

DIFFICULTIES = (("EASY PEASY", "Easy Peasy"), ("SO SO", "So so"), ("DIFFICULT", "Difficult"), ("REALLY DIFFICULT", "Really Difficult"))


class Course(models.Model):
    started_learning = models.BooleanField(default=False)
    weight = models.FloatField(default=0)
    name = models.CharField(max_length=100, null=True, blank=True)
    duration = models.DurationField(default=timedelta())
    comment = models.TextField(default="", null=True, blank=True)
    item = models.IntegerField(null=True, blank=True)
    book = models.CharField(max_length=50, choices=BOOKS, null=True, blank=True)
    family = models.CharField(max_length=50, choices=FAMILIES, null=True, blank=True)
    difficulty = models.CharField(max_length=50, choices=DIFFICULTIES, null=True, blank=True)

    def __str__(self):
        return "%s %s" % ('' if self.name is None else self.name, '' if self.item is None else self.item)

    def seen(self):
        return CourseSeen.objects.filter(course=self).count()

    def get_planning_text(self):
        return "{} - ({}) - {}".format(str(self), self.seen(), self.family.capitalize())

    def simulate_this_course_is_seen(self, today_date, courses):
        self.started_learning = True
        course_seen = CourseSeen()
        course_seen.course = self
        course_seen.date = today_date
        courses.append(course_seen)

        # if self.first_learning_date is None:
        #     self.first_learning_date = today_date
        # elif self.second_learning_date is None:
        #     self.second_learning_date = today_date
        # elif self.third_learning_date is None:
        #     self.third_learning_date = today_date
        # elif self.fourth_learning_date is None:
        #     self.fourth_learning_date = today_date
        # elif self.fifth_learning_date is None:
        #     self.fifth_learning_date = today_date


class CourseSeen(models.Model):
    date = models.DateField(default=datetime.now)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)

    def get_course(self):
        item = self.course.item or ''
        name = self.course.name or ''
        return item + name


class AvailableTime(models.Model):
    date = models.DateField(null=True, blank=True)

    duration = models.DurationField(default=timedelta())

    def __str__(self):
        return datetime.strftime(datetime.combine(self.date, datetime.min.time())
, "%Y-%m-%d")
