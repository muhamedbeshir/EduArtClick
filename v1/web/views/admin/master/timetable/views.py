from datetime import timedelta
import json
from django.core.serializers import serialize
from typing import Any, Dict
from django import views
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils import timezone
from v1.db.master.class_classroom import ClassClassroom
from v1.db.master.school import School
from v1.db.master.school_class import SchoolClass
from v1.db.master.class_time_table import ClassTimeTable
from v1.db.master.school_course import SchoolCourse
from v1.db.master.school_room import SchoolRoom
from v1.db.master.school_schedule import SchoolSchedule
from v1.db.user.profile import TeacherUserProfile
from v1.web.utils import CHECK_USER_PERMISSION
from .forms import ClassTimeTableForm, ClasssTimeTableForm


class CreateClassTimeTable(PermissionRequiredMixin, CreateView):
    permission_required = ('db.add_classtimetable',)
    template_name = 'admin/master/timetable/add.html'
    model = ClassTimeTable
    form_class = ClassTimeTableForm

    def get_success_url(self) -> str:
        return reverse_lazy('web:details_school_course', kwargs={'pk': self.object.ref_course.pk})

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('pk')
        context['title'] = 'Add Class Time Table'
        context['course_id'] = course_id
        course = get_object_or_404(SchoolCourse, pk=course_id)
        CHECK_USER_PERMISSION(self.request, course.ref_school)
        return context

    def get_form_kwargs(self):
        context = super().get_form_kwargs()
        context['course_id'] = self.kwargs.get('pk')
        # context.update(self.kwargs)
        return context

    def form_valid(self, form):
        # context = self.get_context_data()
        # school_id = context['school_id']

        obj = form.save(commit=False)

        # Checking Class Schedule
        school_class = get_object_or_404(SchoolClass, pk=obj.ref_class.pk)
        class_day = obj.class_date.strftime('%A')
        class_days = school_class.ref_day_list.split(", ")

        # if obj.start_time == school_class.ref_schedule.start_time and obj.end_time == school_class.ref_schedule.end_time and class_day in class_days:
        #     msg = f'Time Table "{obj.ref_class}, {obj.class_date}" already exists.'
        #     form.add_error('', msg)
        #     return super().form_invalid(form)

        try:
            # Assign School object obj.ref_school
            obj.ref_school = school_class.ref_school
            obj.save()
            msg = f'Time Table "{obj}" added successfully.'
            print(f'[+] {msg}')
            messages.success(self.request, msg)
        except IntegrityError:
            msg = f'Time Table "{obj.ref_class}, {obj.class_date}" already exists.'
            form.add_error('', msg)
            return super().form_invalid(form)

        return super().form_valid(form)


class UpdateClassTimeTable(PermissionRequiredMixin, UpdateView):
    permission_required = ('db.change_classtimetable',)
    template_name = 'admin/master/timetable/add.html'
    model = ClassTimeTable
    form_class = ClassTimeTableForm

    def get_success_url(self) -> str:
        return reverse_lazy('web:deatil_school', kwargs={'pk': self.object.ref_school.pk})

    def get_context_data(self, **kwargs: Any):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update School Time Table'
        context['school_id'] = self.object.ref_school.pk
        return context

    def get_form_kwargs(self):
        context = super().get_form_kwargs()
        context['school_id'] = self.kwargs.get('pk')
        # context.update(self.kwargs)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        school_id = context['school_id']

        obj = form.save(commit=False)
        try:
            # Assign School object obj.ref_school
            obj.ref_school = get_object_or_404(School, pk=school_id)
            obj.save()
            msg = f'Time Table "{obj}" updated successfully.'
            print(f'[+] {msg}')
            messages.success(self.request, msg)
        except IntegrityError:
            msg = f'Time Table "{obj.ref_class}, {obj.class_date}" already exists.'
            form.add_error('', msg)
            return super().form_invalid(form)

        return super().form_valid(form)


class DeleteClassTimeTable(PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_classtimetable',)
    template_name = 'admin/master/delete_city.html'
    model = ClassTimeTable
    pk_url_kwarg = 'pk'

    def get_success_url(self) -> str:
        return reverse_lazy('web:deatil_school', kwargs={'pk': self.object.ref_school.pk})

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete School Time Table'
        context['content'] = 'Are you sure you want to delete ?'
        return context


def get_classes(request):
    course_id = request.GET.get('course')

    if not course_id:
        return render(request, 'admin/master/classes_dropdown_list_options.html', {'classess': []})

    classess = SchoolClass.objects.filter(ref_course__pk=course_id)

    return render(request, 'admin/master/classes_dropdown_list_options.html', {'classess': classess})


def get_class_timetable(request):
    class_id = request.GET.get('class')

    if not class_id:
        return JsonResponse({})

    classess = get_object_or_404(SchoolClass, pk=class_id)

    course_days = classess.ref_day_list
    class_days = []

    for day_ in course_days.split(", "):
        if day_ == 'Sunday':
            class_days.append(0)
        elif day_ == 'Monday':
            class_days.append(1)
        elif day_ == 'Tuesday':
            class_days.append(2)
        elif day_ == 'Wednesday':
            class_days.append(3)
        elif day_ == 'Thursday':
            class_days.append(4)
        elif day_ == 'Friday':
            class_days.append(5)
        elif day_ == 'Saturday':
            class_days.append(6)

    return JsonResponse({
        "days": classess.ref_day_list.split(', '),
        "class_days": class_days,
        "start_date": classess.summar_start,
        "end_date": classess.summar_end,
        "start_time": classess.ref_schedule.start_time,
        "end_time": classess.ref_schedule.end_time,
    })


def DATE_BETWEEN_DATES(start_date, end_date):
    for x in range((end_date-start_date).days + 1):
        yield start_date+timedelta(days=x)

class CreateClasssTimeTable(CreateView):
    # permission_required = ('db.add_classtimetable',)
    template_name = 'admin/master/class/timetable/add.html'
    model = ClassClassroom
    form_class = ClasssTimeTableForm

    def get_success_url(self) -> str:
        return reverse_lazy('web:detail_school_course', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        s_class = get_object_or_404(SchoolClass, pk=self.kwargs['pk'])
        context['title'] = 'Update Class Time Tables'
        context['class'] = s_class
        context['today'] = timezone.now().date() if timezone.now().date() > s_class.summar_start else s_class.summar_start
        return context
    
    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['class_id'] = self.kwargs['pk']
        return kwargs
    

    def form_valid(self, form):
        class_id = self.kwargs['pk']

        cleaned_data = form.cleaned_data
        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']
        schedule = cleaned_data['ref_schedule']
        classroom = cleaned_data['ref_room']
        teacher = cleaned_data['ref_teacher']


        my_class = get_object_or_404(SchoolClass, pk=class_id)
        class_days = my_class.days_list
        all_dates = DATE_BETWEEN_DATES(start_date, end_date)
        course_dates = filter(lambda x: x.strftime("%A") in class_days, all_dates)

        obj = form.save(commit=False)
        try:
            # Assign class object obj.ref_class
            for course_date in course_dates:
                # print(course_date)
                time_table = get_object_or_404(self.model, class_date=course_date, ref_class=my_class)
                time_table.ref_schedule = schedule
                time_table.ref_teacher = teacher
                if classroom:
                    time_table.ref_room = classroom 
                time_table.save()
           
            msg = f'Time Table "{obj}" added successfully.'
            print(f'[+] {msg}')
            messages.success(self.request, msg)

        except IntegrityError:
            msg = f'Time Table "{obj.ref_class}, {obj.class_date}" already exists.'
            form.add_error('', msg)
            return super().form_invalid(form)
        
        return_url = reverse_lazy('web:detail_school_course', kwargs={'pk': my_class.pk})
        
        return redirect(return_url)


def check_available_schedule(request):
    class_id = request.GET.get('class_id', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    schedule = request.GET.get('schedule', '')

    s_class = get_object_or_404(SchoolClass, pk=class_id)
    # schedule_queryset = SchoolSchedule.objects.filter(ref_school=s_class.ref_school, pk=schedule)

    # queryset = ClassClassroom.objects.filter(ref_class__ref_school=s_class.ref_school, class_date__gte=start_date, class_date__lte=end_date).order_by('ref_schedule').values_list('ref_schedule', flat=True).distinct('ref_schedule')
    
    queryset = ClassClassroom.objects.filter(ref_class__ref_school=s_class.ref_school, class_date__gte=start_date, class_date__lte=end_date)

    queryset = queryset.filter(ref_schedule__pk=schedule).exclude(ref_class=s_class)
    '''
        If queryset, returns data means classroom reserved on that schedule,
        else, their is not classroom revesed on that schedule means that schedule is available
    '''
    if queryset:
        queryset_room = queryset.order_by('ref_room').values_list('ref_room', flat=True)
        queryset_teacher = queryset.order_by('ref_teacher').values_list('ref_teacher', flat=True).exclude()
        
        classrooms = SchoolRoom.objects.filter(ref_school=s_class.ref_school, minimum__lte=s_class.minimum, capacity__gte=s_class.maximum).exclude(pk__in=queryset_room)

        teachers = TeacherUserProfile.objects.filter(ref_school=s_class.ref_school).exclude(ref_user__id__in=queryset_teacher)
    else:
        classrooms = SchoolRoom.objects.filter(ref_school=s_class.ref_school, minimum__lte=s_class.minimum, capacity__gte=s_class.maximum)
        teachers = TeacherUserProfile.objects.filter(ref_school=s_class.ref_school)

    room_serialized_data = serialize("json", classrooms)
    room_serialized_data = json.loads(room_serialized_data)
    
    teacher_serialized_data = serialize("json", teachers)
    teacher_serialized_data = json.loads(teacher_serialized_data)

    return JsonResponse({'rooms': room_serialized_data, 'teachers': teacher_serialized_data}, safe=False)
    