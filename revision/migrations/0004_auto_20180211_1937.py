# Generated by Django 2.0.2 on 2018-02-11 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revision', '0003_auto_20180211_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabletime',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='course',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='course',
            name='fifth_learning_date',
        ),
        migrations.RemoveField(
            model_name='course',
            name='first_learning_date',
        ),
        migrations.RemoveField(
            model_name='course',
            name='fourth_learning_date',
        ),
        migrations.RemoveField(
            model_name='course',
            name='name',
        ),
        migrations.RemoveField(
            model_name='course',
            name='second_learning_date',
        ),
        migrations.RemoveField(
            model_name='course',
            name='seen',
        ),
        migrations.RemoveField(
            model_name='course',
            name='started_learning',
        ),
        migrations.RemoveField(
            model_name='course',
            name='third_learning_date',
        ),
        migrations.RemoveField(
            model_name='course',
            name='weight',
        ),
    ]
