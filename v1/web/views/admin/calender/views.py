import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, CreateView, View
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse


from v1.db.models import *
from .utils import Calendar


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, View):
    template_name = "admin/calendar/calendar.html"

    def get(self, request, *args, **kwargs):
        event_list = []
        colors_list = ["Red", "Orange", "Blue", "Green", "Black", "Brown", "Purple", "Pink", "Cyan", "Lime", "Aqua", "Azure", "Maroon", "Magenta", "Coral", "Indigo", "Beige", "Crimson", "Violet", "Lavender", "Olive"]
        count = 0

        user = request.user.schoolstudentuserprofile.id
        events = StudentProfileHasCourse.objects.filter(ref_student=user)

        for event in events:
            # class_days = event.ref_course.ref_day_list.split(", ")
            # start_date = event.start_date
            # end_date = event.end_date

            # all_dates = date_between_dates(start_date, end_date)
            # class_dates = filter(lambda x: x.strftime("%A")
            #                      in class_days, all_dates)
            class_dates = ClassClassroom.objects.filter(ref_class=event.ref_course)

            if count == len(colors_list):
                count = 0
            color_name = colors_list[count]
            count += 1

            updated_class_time_tables = ClassTimeTable.objects.filter(
                ref_class=event.ref_course)
            updated_class_dates = []
            for class_time_table in updated_class_time_tables:
                updated_class_dates.append({
                    "class_date": class_time_table.class_date,
                    "start_time": class_time_table.start_time,
                    "end_time": class_time_table.end_time,
                })

            for class_date in class_dates:
                data_dict = {
                    "title": event.title,
                    "start": class_date.class_date,
                    # "end": event.summar_end,
                    "schedule": class_date.ref_schedule,
                    "start_time": class_date.ref_schedule.start_time.strftime("%H:%M:%S"),
                    "end_time": class_date.ref_schedule.end_time.strftime("%H:%M:%S"),
                    "teacher": class_date.teacher_fullname,
                    "room": class_date.ref_room.name,
                    "color": color_name,
                }

                updated_class_times = list(filter(
                    lambda update_class: update_class['class_date'] == class_date, updated_class_dates))
                if updated_class_times:
                    data_dict["schedule"] = f'{updated_class_times[0]["start_time"].strftime("%I:%M %p")} - {updated_class_times[0]["end_time"].strftime("%I:%M %p")}'
                    data_dict["start_time"] = updated_class_times[0]["start_time"]
                    data_dict["end_time"] = updated_class_times[0]["end_time"]

                event_list.append(
                    data_dict
                )
        context = {"events": event_list}
        print(context)
        return render(request, self.template_name, context)


class SchoolCalendarView(LoginRequiredMixin, View):
    template_name = "admin/calendar/calendar.html"

    def get(self, request, *args, **kwargs):
        event_list = []
        colors_list = ["Red", "Orange", "Blue", "Green", "Black", "Brown", "Purple", "Pink", "Cyan", "Lime", "Aqua", "Azure", "Maroon", "Magenta", "Coral", "Indigo", "Beige", "Crimson", "Violet", "Lavender", "Olive"]
        count = 0
        user = request.user

        organization_user = get_object_or_404(OrganizationUserProfile, ref_user=user)

        events = SchoolClass.objects.filter(ref_school=organization_user.ref_school)
        # class_dates = ClassClassroom.objects.filter(ref_class__in=event)
        for event in events:
            # class_days = event.ref_day_list.split(", ")
            # start_date = event.summar_start
            # end_date = event.summar_end

            # all_dates = date_between_dates(start_date, end_date)
            # class_dates = filter(lambda x: x.strftime("%A") in class_days, all_dates)
            class_dates = ClassClassroom.objects.filter(ref_class=event)#.values_list('class_date', flat=True)

            if count == len(colors_list):
                count = 0
            color_name = colors_list[count]
            count += 1

            updated_class_time_tables = ClassTimeTable.objects.filter(ref_class=event)
            updated_class_dates = []
            for class_time_table in updated_class_time_tables:
                updated_class_dates.append({
                    "class_date": class_time_table.class_date,
                    "start_time": class_time_table.start_time,
                    "end_time": class_time_table.end_time,
                })

            for class_date in class_dates:
                data_dict = {
                    "title": event.title,
                    "start": class_date.class_date,
                    # "end": event.summar_end,
                    "schedule": class_date.ref_schedule,
                    "start_time": class_date.ref_schedule.start_time.strftime("%H:%M:%S"),
                    "end_time": class_date.ref_schedule.end_time.strftime("%H:%M:%S"),
                    "teacher": class_date.teacher_fullname,
                    "room": class_date.ref_room.name,
                    "color": color_name,
                }

                updated_class_times = list(filter(
                    lambda update_class: update_class['class_date'] == class_date, updated_class_dates))
                if updated_class_times:
                    data_dict["schedule"] = f'{updated_class_times[0]["start_time"].strftime("%I:%M %p")} - {updated_class_times[0]["end_time"].strftime("%I:%M %p")}'
                    data_dict["start_time"] = updated_class_times[0]["start_time"]
                    data_dict["end_time"] = updated_class_times[0]["end_time"]

                event_list.append(
                    data_dict
                )
        context = {"events": event_list}

        return render(request, self.template_name, context)


class TeacherCalendarView(LoginRequiredMixin, View):
    template_name = "admin/calendar/calendar.html"

    def get(self, request, *args, **kwargs):
        event_list = []
        colors_list = ["Red", "Orange", "Blue", "Green", "Black", "Brown", "Purple", "Pink", "Cyan", "Lime", "Aqua", "Azure", "Maroon", "Magenta", "Coral", "Indigo", "Beige", "Crimson", "Violet", "Lavender", "Olive"]
        count = 0

        user = request.user
        events = SchoolClass.objects.filter(ref_teacher_name=user)
        
        for event in events:
            class_dates = ClassClassroom.objects.filter(ref_class=event)
            if count == len(colors_list):
                count = 0
            color_name = colors_list[count]
            count += 1

            updated_class_time_tables = ClassTimeTable.objects.filter(
                ref_class=event)
            updated_class_dates = []
            for class_time_table in updated_class_time_tables:
                updated_class_dates.append({
                    "class_date": class_time_table.class_date,
                    "start_time": class_time_table.start_time,
                    "end_time": class_time_table.end_time,
                })

            for class_date in class_dates:
                if not user == class_date.ref_teacher:
                    continue

                data_dict = {
                    "title": event.title,
                    "start": class_date.class_date,
                    # "end": event.summar_end,
                    "schedule": class_date.ref_schedule,
                    "start_time": class_date.ref_schedule.start_time.strftime("%H:%M:%S"),
                    "end_time": class_date.ref_schedule.end_time.strftime("%H:%M:%S"),
                    "teacher": class_date.teacher_fullname,
                    "room": class_date.ref_room.name,
                    "color": color_name,
                }


                updated_class_times = list(filter(
                    lambda update_class: update_class['class_date'] == class_date, updated_class_dates))
                if updated_class_times:
                    data_dict["schedule"] = f'{updated_class_times[0]["start_time"].strftime("%I:%M %p")} - {updated_class_times[0]["end_time"].strftime("%I:%M %p")}'
                    data_dict["start_time"] = updated_class_times[0]["start_time"]
                    data_dict["end_time"] = updated_class_times[0]["end_time"]

                event_list.append(
                    data_dict
                )
        context = {"events": event_list}

        return render(request, self.template_name, context)


def date_between_dates(start_date, end_date):
    for x in range((end_date-start_date).days):
        yield start_date+timedelta(days=x)
