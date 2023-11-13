from datetime import date, timedelta
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Max, Min
from v1.db.master.class_classroom import ClassClassroom
from v1.db.master.class_time_table import ClassTimeTable
from v1.db.master.school import School
from v1.db.master.school_class_installment import SchoolClassInstallment
from v1.db.master.school_course import SchoolCourse
from v1.db.master.school_course_price import SchoolCoursePrice
from v1.db.master.school_schedule import SchoolSchedule

from v1.db.models import SchoolClass
from v1.db.other.week_day import WeekDayList
from v1.db.user.profile import TeacherUserProfile
from v1.db.user.student_profile_has_course import StudentProfileHasCourse
from v1.web.utils import CHECK_USER_PERMISSION
from v1.web.views.admin.master.school.forms import SchoolCoursePriceForm
from django.core.exceptions import PermissionDenied
from .forms import SchoolClassEditForm, SchoolClassForm

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError

current_day = date.today()
previous_day = date.today() - timedelta(days=1)

def DATE_BETWEEN_DATES(start_date, end_date):
    for x in range((end_date-start_date).days + 1):
        yield start_date+timedelta(days=x)


@login_required
@permission_required(['db.add_schoolclass'], raise_exception=True)
def create_school_class(request, pk):
    user = request.user
    raise_permission_denied = False

    m_course = get_object_or_404(SchoolCourse, pk=pk)
    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            school = m_course.ref_school
            if logged_in_user == school.id:

                context = {}

                school = m_course.ref_school
                # school = school.first()

                PriceFormset = modelformset_factory(
                    SchoolCoursePrice, form=SchoolCoursePriceForm)

                form = SchoolClassForm(
                    request.POST or None, logged_in_user=logged_in_user)
                # print(form)
                formset = PriceFormset(
                    request.POST or None, queryset=SchoolCoursePrice.objects.none(), prefix='price')
                teachers = TeacherUserProfile.objects.filter(
                    ref_school=school.id)
                schedules = SchoolSchedule.objects.filter(ref_school=school.id)
                days = WeekDayList.objects.all()
                # print(teachers)

                data = request.POST.dict()
                if request.method == 'POST':
                    day_names = [x.name for x in WeekDayList.objects.all()]
                    day_ids = []
                    for x in day_names:
                        day_ids.append(int(request.POST.get(x))) if request.POST.get(
                            x) else print("racel")
                    # print(day_ids)
                    # ref_day = request.POST.get(ref_day)
                    if form.is_valid() and formset.is_valid():
                        try:
                            with transaction.atomic():
                                course = form.save(commit=False)

                                if request.FILES.get('document'):
                                    course.document = request.FILES['document']

                                course.ref_course = m_course
                                course.ref_school = school
                                course.save()
                                for x in day_ids:
                                    course.ref_day.add(
                                        WeekDayList.objects.get(id=x))
                                for price in formset:
                                    data = price.save(commit=False)
                                    data.ref_school_course = course  # .ref_course
                                    data.save()

                                # Assign Course Classroom
                                class_days = course.days_list
                                all_dates = DATE_BETWEEN_DATES(course.summar_start, course.summar_end)
                                course_dates = filter(lambda x: x.strftime("%A") in class_days, all_dates)

                                # SCCRObjects = []
                                for course_date in course_dates:
                                    # SCCRObjects.append(
                                    ClassClassroom.objects.create(
                                        ref_class=course,
                                        ref_teacher=course.ref_teacher_name,
                                        ref_room = course.ref_room,
                                        ref_schedule=course.ref_schedule,
                                        class_date=course_date,
                                    )
                                    # )

                                # ClassClassroom.objects.bulk_create(SCCRObjects)
                                # End Assign Course Classroom

                                print("Successfully =====================")
                                return redirect('web:details_school_course', pk=m_course.pk)
                        except IntegrityError:
                            error = "School Teacher Schedule should be unique."
                            form.add_error(None, error)
                    else:
                        print("form=====================Error=============")
                        print(form.errors)

                context['course'] = m_course
                context['school'] = school
                context['teachers'] = teachers
                context['schedules'] = schedules
                context['days'] = days
                context['form'] = form
                context['formset'] = formset
                context['cdate'] = current_day
                context['pdate'] = previous_day

                print(context)
                return render(request, 'admin/master/class/create_school_class.html', context)
            else:
                raise_permission_denied = True

        except School.DoesNotExist:
            raise_permission_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            school = m_course.ref_school
            if school.id:

                context = {}

                # school = School.objects.filter(pk=pk)
                # school = school.first()

                PriceFormset = modelformset_factory(
                    SchoolCoursePrice, form=SchoolCoursePriceForm)

                form = SchoolClassForm(
                    request.POST or None, logged_in_user=school.id)
                # print(form)
                formset = PriceFormset(
                    request.POST or None, queryset=SchoolCoursePrice.objects.none(), prefix='price')
                teachers = TeacherUserProfile.objects.filter(
                    ref_school=school.id)
                schedules = SchoolSchedule.objects.filter(ref_school=school.id)
                days = WeekDayList.objects.all()
                # print(teachers)

                data = request.POST.dict()
                if request.method == 'POST':
                    day_names = [x.name for x in WeekDayList.objects.all()]
                    day_ids = []
                    for x in day_names:
                        day_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("racel")
                    # print(day_ids)
                    # ref_day = request.POST.get(ref_day)
                    if form.is_valid() and formset.is_valid():
                        try:
                            with transaction.atomic():
                                course = form.save(commit=False)
                                print('course ==> ', course)
                                if request.FILES.get('document'):
                                    course.document = request.FILES['document']

                                course.ref_course = m_course
                                course.ref_school = school
                                course.save()
                                print(course.ref_school)
                                print(course.ref_course)
                                for x in day_ids:
                                    course.ref_day.add(
                                        WeekDayList.objects.get(id=x))

                                for price in formset:
                                    data = price.save(commit=False)
                                    data.ref_school_course = course  # course
                                    data.save()

                                # Assign Course Classroom
                                class_days = course.days_list
                                all_dates = DATE_BETWEEN_DATES(course.summar_start, course.summar_end)
                                course_dates = filter(lambda x: x.strftime("%A") in class_days, all_dates)

                                # SCCRObjects = []
                                for course_date in course_dates:
                                    # SCCRObjects.append(
                                    ClassClassroom.objects.create(
                                        ref_class=course,
                                        ref_teacher=course.ref_teacher_name,
                                        ref_room = course.ref_room,
                                        ref_schedule=course.ref_schedule,
                                        class_date=course_date,
                                    )
                                    # )

                                # ClassClassroom.objects.bulk_create(SCCRObjects)
                                # End Assign Course Classroom

                                print("Successfully =====================")
                                return redirect('web:details_school_course', pk=m_course.pk)
                        except IntegrityError:
                            error = "School Teacher Schedule should be unique."
                            form.add_error(None, error)
                    else:
                        print("form=====================Error=============")
                        print(form.errors)

                context['course'] = m_course
                context['school'] = school
                context['teachers'] = teachers
                context['schedules'] = schedules
                context['days'] = days
                context['form'] = form
                context['formset'] = formset
                context['cdate'] = current_day
                context['pdate'] = previous_day

                print(context)
                return render(request, 'admin/master/class/create_school_class.html', context)
            else:
                raise_permission_denied = True

        except School.DoesNotExist:
            raise_permission_denied = True

    else:
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()

@login_required
@permission_required(['db.change_schoolclass'], raise_exception=True)
def update_school_class(request, pk):
    template_name = 'admin/master/class/edit_school_class.html'
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            queryset = SchoolClass.objects.get(id=pk)
            if logged_in_user == queryset.ref_school.id:
                data = request.POST.dict()
                print('<=>'*10, data)
                form = SchoolClassForm(
                    request.POST or None, instance=queryset, logged_in_user=logged_in_user)
                if request.method == 'POST':
                    print(request.POST)
                    form = SchoolClassEditForm(request.POST, instance=queryset)
                    # print(form)
                    if form.is_valid():
                        print(form.cleaned_data)
                        obj = form.save(commit=False)

                        if request.FILES.get('document'):
                            obj.document = request.FILES['document']

                        obj.save()
                        print("Successfully edit data")
                        return redirect('web:deatil_school', pk=queryset.ref_school.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = SchoolClassForm(
                        request.POST or None, instance=queryset, logged_in_user=logged_in_user)

                kwvars = {
                    'school': queryset.ref_school,
                    'course': queryset,
                    'form': form,
                    'cdate': current_day, 'pdate': previous_day
                }

                return render(request, template_name, kwvars)

            else:
                raise_permission_denied = True
        except SchoolClass.DoesNotExist:
            raise_permission_denied = True

    elif user.groups.filter(name='teacher').exists():
        logged_in_user = request.user
        try:
            queryset = SchoolClass.objects.get(id=pk)
            if logged_in_user == queryset.ref_teacher_name:
                form = SchoolClassForm(
                    instance=queryset, logged_in_user=logged_in_user, user_type="teacher")
                if request.method == 'POST':
                    form = SchoolClassForm(request.POST, instance=queryset)
                    print(form)
                    if form.is_valid():
                        form.save()
                        print("Successfully edit data")
                        return redirect('web:deatil_school', pk=queryset.ref_school.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = SchoolClassForm(
                        instance=queryset, logged_in_user=logged_in_user, user_type="teacher")

                kwvars = {
                    'school': queryset.ref_school,
                    'course': queryset,
                    'form': form,
                    'cdate': current_day, 'pdate': previous_day
                }

                return render(request, template_name, kwvars)

            else:
                raise_permission_denied = True
        except Exception as e:  # SchoolCourse.DoesNotExist:
            raise_permission_denied = True

    else:
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


# class SchoolCourseUpdateView(LoginRequiredMixin, UpdateView):
#     model = SchoolCourse
#     form_class = SchoolCourseForm
#     template_name = 'admin/master/class/create_school_class.html'
#     pk_url_kwarg = 'pk'

#     def __init__(self):
#         super().__init__()
#         self.PriceFormset = formset_factory(SchoolCoursePriceForm)

#     def get_success_url(self):
#         return reverse('web:deatil_school', args=(self.object.ref_school.id,))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         courseprice = list(SchoolCoursePrice.objects.filter(ref_school_course=self.object.id).values('min_weak', 'max_weak', 'price'))

#         context['formset'] = self.PriceFormset(prefix='rel_ref_school_school_course', initial=courseprice)
#         context['title'] = "Edit"
#         return context

#     def form_valid(self, form):
#     	user=request.user
#     	print(user)
#     	instance = form.save()
#     	formset = self.PriceFormset(self.request.POST, prefix='rel_ref_school_school_course')
#     	if formset.is_valid():
#     		print('formset')
#     		total_forms = int(formset.data.get('rel_ref_school_school_course-TOTAL_FORMS'))
#     		if total_forms > 0:
#     			SchoolCoursePrice.objects.filter(ref_school_course=self.object.id).delete()
#     			for i in range(total_forms):

#     				price = formset.data.get('rel_ref_school_school_course-' + str(i) + '-price')
#     				min_weak = formset.data.get('rel_ref_school_school_course-' + str(i) + '-min_weak')
#     				max_weak = formset.data.get('rel_ref_school_school_course-' + str(i) + '-max_weak')
#     				if price and min_weak:
#     					courseprice = SchoolCoursePrice(price=price, min_weak=min_weak, max_weak=max_weak, ref_school_course=instance)
#     					courseprice.save()
#     	messages.success(self.request, 'Successfully Update.')
#     	return super(SchoolCourseUpdateView, self).form_valid(form)


def create_school_course_price(request, pk):
    course = SchoolClass.objects.filter(pk=pk)
    course = course.first()
    context = {}

    # print(course.ref_school.id)

    PriceFormset = modelformset_factory(
        SchoolCoursePrice, form=SchoolCoursePriceForm)
    formset = PriceFormset(request.POST or None, queryset=SchoolClass.objects.none(
    ), prefix='rel_ref_school_school_course')
    if request.method == 'POST':
        if formset.is_valid():
            try:
                with transaction.atomic():
                    for course_price_info in formset:
                        data = course_price_info.save(commit=False)
                        data.ref_school_course = course
                        data.save()
            except IntegrityError:
                print("Error Encountered")
            return redirect('web:deatil_school', pk=course.ref_school.id)

    context['formset'] = formset
    context['course'] = course
    return render(request, 'admin/master/course/course_price.html', context)


class SchoolClassDetails(PermissionRequiredMixin, DetailView):
    permission_required = ('db.view_schoolclass',)
    model = SchoolClass
    context_object_name = 'course'
    template_name = 'admin/course/details.html'

    def get_user(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        print(self.object)
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        user = self.get_user()

        if user.groups.filter(name='school').exists():
            course_id = self.kwargs.get('pk', None)
            print('COURSE_ID :: ', course_id)
            course_query = SchoolClass.objects.filter(
                id=course_id, ref_school=user.organizationuserprofile.ref_school)
            timetables = ClassTimeTable.objects.filter(
                ref_class__in=course_query)
            installments = SchoolClassInstallment.objects.filter(
                ref_class=course_id)
            class_classrooms = ClassClassroom.objects.filter(ref_class=course_id)

            if course_query.exists():
                course = course_query.get()

                context = super(__class__, self).get_context_data(**kwargs)
                context["course"] = course
                context['price'] = SchoolCoursePrice.objects.filter(
                    ref_school_course=course).order_by("id")
                # context['price'] = SchoolCoursePrice.objects.filter(
                #     ref_school_course=course.ref_course).order_by("id")
                context['student'] = StudentProfileHasCourse.objects.filter(
                    ref_course=course).order_by("pk")
                context["timetables"] = timetables
                context["installments"] = installments
                context["class_classrooms"] = class_classrooms
                return context

        elif user.groups.filter(name='teacher').exists():
            course_id = self.kwargs.get('pk', None)
            # course_query = SchoolCourse.objects.filter(
            #     id=course_id, ref_teacher_name=user)
            course_query = SchoolClass.objects.filter(
                id=course_id, ref_teacher_name=user)
            if course_query.exists():
                course = course_query.get()

                context = super(__class__, self).get_context_data(**kwargs)
                context["course"] = course
                context['price'] = SchoolCoursePrice.objects.filter(
                    ref_school_course=course).order_by("id")
                context['student'] = StudentProfileHasCourse.objects.filter(
                    ref_course=course).order_by("id")
                context["timetables"] = []
                context["installments"] = []
                return context

        elif user.groups.filter(name='admin').exists() or user.is_superuser:
            course_id = self.kwargs.get('pk', None)

            course_query = SchoolClass.objects.filter(id=course_id)
            timetables = ClassTimeTable.objects.filter(
                ref_class__in=course_query)
            installments = SchoolClassInstallment.objects.filter(
                ref_class=course_id)
            class_classrooms = ClassClassroom.objects.filter(ref_class=course_id)

            if course_query.exists():
                course = course_query.get()
                context = super(__class__, self).get_context_data(**kwargs)
                context["course"] = course
                context['price'] = SchoolCoursePrice.objects.filter(
                    ref_school_course=course).order_by("id")
                context['student'] = StudentProfileHasCourse.objects.filter(
                    ref_course=course).order_by("id")
                context["timetables"] = timetables
                context["installments"] = installments
                context["class_classrooms"] = class_classrooms
                return context


        raise PermissionDenied()



class DeleteSchoolClass(PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_schoolclass',)
    model = SchoolClass
    template_name = 'admin/master/delete_school_course.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:details_school_course', args=(self.object.ref_course.id,))

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete School Class'
        context['content'] = 'Are you sure you want to delete ?'
        return context
