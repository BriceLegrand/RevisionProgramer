import datetime

from revision.models import AvailableTime, Course


def populate_courses():
    DIFF = ["EASY PEASY", "SO SO", "DIFFICULT", "REALLY DIFFICULT"]
    from datetime import timedelta
    from revision.models import Course
    f = open(r"C:\Users\BriceFixe\Desktop\internat.csv", 'r')
    header = True
    for line in f:
        line = line.replace("\n", "")
        if header:
            header = False
            continue
        line = line.split(";")
        # print(line)
        # c = Course()
        # c.item = line[0] or None
        # c.name = line[1]
        # c.duration = timedelta(minutes=int(line[2]))
        # c.book = line[3]
        # c.family = line[4]
        # c.save()
        print(line[0], line[1])
        print(line)
        if line[0] != '':
            c = Course.objects.get(item=line[0])
        else:
            c = Course.objects.get(name=line[1])

        c.difficulty = DIFF[int(line[5]) - 1]
        print(c.difficulty)
        c.save()
        print(c)
#
# def populate_days():
#     from datetime import datetime
#     from datetime import timedelta
#
#     from revision.models import AvailableTime
#
#     av = [0, 2, 0, 2, 7, 6, 6]
#     today = datetime(2018, 2, 12)
#     for i in range(400):
#         timeAv = AvailableTime()
#         timeAv.duration = timedelta(hours=av[i % 7])
#         timeAv.date = today
#         today = today + timedelta(days=1)
#         timeAv.save()


def update_summer_days():
    days = {0: 2, 1: 8, 2:2, 3:8, 4:8, 5:2, 6:2}
    print("cuuuuuuuuuuuuuuuuuu")
    dates = AvailableTime.objects.filter(date__gte="2018-06-01").filter(date__lte="2018-07-31")
    print(dates)
    for date in dates:
        date.duration = datetime.timedelta(hours=days[date.date.weekday()])
        print(date.duration)
        date.save()
    dates = AvailableTime.objects.filter(date__gte="2018-08-01").filter(date__lte="2018-08-31")
    for date in dates:
        date.duration = datetime.timedelta(0)
        date.save()

def get_total_available_time():
    summ= datetime.timedelta(0)
    d = AvailableTime.objects.all().values_list("duration", flat=True)
    for el in d:
        summ+=el
    print(summ)
    c = Course.objects.all().values_list("duration", flat=True)
    summ = datetime.timedelta(0)
    for el in c:
        summ+=el
    print(summ)

# update_summer_days()
populate_courses()


def set_frequency_type():
    #FACILE  0 - 10 - 30 - 90 - 180 - 270 - 360 - 450
    #MOYEN   0 - 3 - 10 - 30 - 90 - 180 - 270 - 360 - 450
    #DIFFICILE 0 - 3 - 10 - 30 - 60 - 90 - 180 - 270 - 360 - 450
    #TRES SAME MAIS EN PREMIER
    FACILE = []
    populate_courses()

