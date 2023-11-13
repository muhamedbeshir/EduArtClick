from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Max, Min
from django.contrib.auth.models import User
from v1.db.master.school_class_installment import SchoolClassInstallment
from v1.db.models import *
from v1.db.user.student_profile_has_service import StudentProfileHasService
from v1.web.utils import CHECK_USER_PERMISSION
from .forms import *
from django.core.exceptions import PermissionDenied
import datetime

from datetime import date, timedelta

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError
import phonenumbers


current_day = date.today()
previous_day = date.today() - timedelta(days=1)


class SchoolStudentDetails(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ('db.view_schoolstudentuserprofile',)
    model = SchoolStudentUserProfile
    context_object_name = 'student'
    template_name = 'admin/master/student/details.html'

    def get_user(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        user = self.get_user()

        if user.groups.filter(name='school').exists():
            student_id = self.kwargs.get('pk', None)
            student_query = SchoolStudentUserProfile.objects.filter(
                id=student_id, ref_school=user.organizationuserprofile.ref_school)
            student_course = StudentProfileHasCourse.objects.filter(
                ref_student=student_id)
            student_accommodation = StudentProfileHasAccommodation.objects.filter(
                ref_student=student_id)
            student_service = StudentProfileHasService.objects.filter(
                ref_student=student_id)
            certificate = SchoolCertificate.objects.filter(
                ref_student=student_id)
            # installments = student_course.first().installments

            if student_query.exists():
                student = student_query.get()
                context = super(__class__, self).get_context_data(**kwargs)
                context["student"] = student
                context["student_course"] = student_course
                context["student_accommodation"] = student_accommodation
                context["student_services"] = student_service
                context["certificate"] = certificate
                # context["installments"] = installments
                return context

        elif user.groups.filter(name='teacher').exists():
            school = self.request.user.teacheruserprofile.ref_school.id
            school_model = School.objects.get(id=school)
            student_id = self.kwargs.get('pk', None)

            student_query = SchoolStudentUserProfile.objects.filter(
                id=student_id, ref_school=school_model)
            student_course = StudentProfileHasCourse.objects.filter(
                ref_student=student_id)
            student_accommodation = StudentProfileHasAccommodation.objects.filter(
                ref_student=student_id)
            student_service = StudentProfileHasService.objects.filter(
                ref_student=student_id)
            # installments = student_course.first().installments

            if student_query.exists():
                student = student_query.get()
                context = super(__class__, self).get_context_data(**kwargs)
                context["student"] = student
                context["student_course"] = student_course
                context["student_accommodation"] = student_accommodation
                context["student_services"] = student_service
                # context["installments"] = installments
                return context

        elif user.groups.filter(name='admin').exists() or user.is_superuser:
            student_id = self.kwargs.get('pk', None)
            student_query = SchoolStudentUserProfile.objects.filter(
                id=student_id)
            student_course = StudentProfileHasCourse.objects.filter(
                ref_student=student_id)
            student_accommodation = StudentProfileHasAccommodation.objects.filter(
                ref_student=student_id)
            student_service = StudentProfileHasService.objects.filter(
                ref_student=student_id)
            certificate = SchoolCertificate.objects.filter(
                ref_student=student_id)
            # installments = student_course.first().installments

            if student_query.exists():
                student = student_query.get()
                context = super(__class__, self).get_context_data(**kwargs)
                context["student"] = student
                context["student_course"] = student_course
                context["student_accommodation"] = student_accommodation
                context["student_services"] = student_service
                context["certificate"] = certificate
                # context["installments"] = installments
                return context

        raise PermissionDenied()


@login_required
@permission_required(['db.change_schoolstudentuserprofile'], raise_exception=True)
def update_school_student(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        # print("===============================================")
        # print(logged_in_user)
        try:
            queryset = SchoolStudentUserProfile.objects.get(id=pk)

            if logged_in_user == queryset.ref_school.id:

                data = request.POST.dict()
                form = UpdateSchoolStudentForm(instance=queryset)
                if request.method == 'POST':
                    form = UpdateSchoolStudentForm(
                        request.POST, instance=queryset)
                    if form.is_valid():
                        ''' Checking valid mobile number using phonenumbers '''
                        phone_number = form.cleaned_data.get('phone')
                        print('Mobile Number: ', phone_number)
                        try:
                            validate_number = phonenumbers.parse(
                                phone_number, None)
                            print(validate_number)
                            if phonenumbers.is_valid_number(validate_number):
                                print('Valid Mobile Number: ', phone_number)
                                student = form.save(commit=False)
                                student.save()
                                print("Successfully edit data")
                                return redirect('web:deatil_school', pk=logged_in_user)
                            else:
                                print('Invalid Mobile Number: ', phone_number)
                                error = f"Please enter a valid mobile number: {phone_number}"
                                form.add_error(None, error)
                        except phonenumbers.phonenumberutil.NumberParseException:
                            print(
                                "phonenumbers.phonenumberutil.NumberParseException")
                            error = f"Please enter a valid mobile number: {phone_number}"
                            form.add_error(None, error)
                            print(form.errors)

                        # student = form.save(commit=False)
                        # student.save()
                        # print("Successfully edit data")
                        # return redirect('web:deatil_school', pk=logged_in_user)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                        print(form.errors)
                else:
                    form = UpdateSchoolStudentForm(instance=queryset)

                template_name = 'admin/master/student/edit_student.html'
                kwvars = {
                    'student': queryset,
                    'form': form,
                    'cdate': current_day, 'pdate': previous_day
                }

                return render(request, template_name, kwvars)
            else:
                raise_permission_denied = True
        except:
            raise_permission_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            queryset = SchoolStudentUserProfile.objects.get(id=pk)

            if queryset.ref_school.id:

                data = request.POST.dict()
                form = UpdateSchoolStudentForm(instance=queryset)
                if request.method == 'POST':
                    form = UpdateSchoolStudentForm(
                        request.POST, instance=queryset)
                    if form.is_valid():
                        ''' Checking valid mobile number using phonenumbers '''
                        phone_number = form.cleaned_data.get('phone')
                        print('Mobile Number: ', phone_number)
                        try:
                            validate_number = phonenumbers.parse(
                                phone_number, None)
                            print(validate_number)
                            if phonenumbers.is_valid_number(validate_number):
                                print('Valid Mobile Number: ', phone_number)
                                student = form.save(commit=False)
                                student.save()
                                print("Successfully edit data")
                                return redirect('web:deatil_school', pk=queryset.ref_school.id)
                            else:
                                print('Invalid Mobile Number: ', phone_number)
                                error = f"Please enter a valid mobile number: {phone_number}"
                                form.add_error(None, error)
                        except phonenumbers.phonenumberutil.NumberParseException:
                            print(
                                "phonenumbers.phonenumberutil.NumberParseException")
                            error = f"Please enter a valid mobile number: {phone_number}"
                            form.add_error(None, error)
                            print(form.errors)

                        # student = form.save(commit=False)
                        # student.save()
                        # print("Successfully edit data")
                        # return redirect('web:deatil_school', pk=queryset.ref_school.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                        print(form.errors)
                else:
                    form = UpdateSchoolStudentForm(instance=queryset)

                template_name = 'admin/master/student/edit_student.html'
                kwvars = {
                    'student': queryset,
                    'form': form,
                    'cdate': current_day, 'pdate': previous_day
                }

                return render(request, template_name, kwvars)
            else:
                raise_permission_denied = True
        except:
            raise_permission_denied = True

    else:
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.delete_schoolstudentuserprofile'], raise_exception=True)
def delete_school_student(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        # print(logged_in_user)
        try:
            user_id = User.objects.get(id=pk)
            profifile_id = SchoolStudentUserProfile.objects.filter(
                ref_user=user_id.id)
            profifile_id = profifile_id.first()

            if logged_in_user == profifile_id.ref_school.id:
                print("===========")
                if request.method == 'POST':
                    user_id.delete()
                    print("Delete Successfully")
                    return redirect('web:deatil_school', pk=request.user.organizationuserprofile.ref_school.id)
                return render(request, 'admin/master/student/delete_school_student.html', {'profifile_id': profifile_id})
            else:
                print("==============================auth error===========")
                raise_permission_denied = True

        except:
            print("==============================try error===========")
            raise_permission_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            user_id = User.objects.get(id=pk)
            profifile_id = SchoolStudentUserProfile.objects.filter(
                ref_user=user_id.id)
            profifile_id = profifile_id.first()

            if profifile_id.ref_school.id:
                print("===========")
                if request.method == 'POST':
                    user_id.delete()
                    print("Delete Successfully")
                    return redirect('web:deatil_school', pk=profifile_id.ref_school.id)
                return render(request, 'admin/master/student/delete_school_student.html', {'profifile_id': profifile_id})
            else:
                print("==============================auth error===========")
                raise_permission_denied = True

        except:
            print("==============================try error===========")
            raise_permission_denied = True

    else:
        print("==============================groups error===========")
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.change_schoolstudentuserprofile'], raise_exception=True)
def update_student_course(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id

        try:
            queryset = StudentProfileHasCourse.objects.get(id=pk)
            # print(logged_in_user)
            print(queryset)
            if logged_in_user == queryset.ref_student.ref_school.id:
                data = request.POST.dict()
                form = StudentProfileHasCourseForm(
                    instance=queryset, logged_in_user=logged_in_user)
                if request.method == 'POST':
                    form = StudentProfileHasCourseForm(
                        request.POST, instance=queryset, logged_in_user=logged_in_user)
                    if form.is_valid():
                        student_course = form.save(commit=False)
                        ref_course = data.get('ref_course')
                        study_period = data.get('study_period')
                        start_date = data.get('start_date')
                        if start_date and study_period:
                            day = (int(study_period) * 7)-3
                            date_1 = datetime.datetime.strptime(
                                start_date, "%Y-%m-%d")
                            date_2 = date_1 + datetime.timedelta(days=day)
                            end_date_new = date_2.strftime('%Y-%m-%d')
                        student_course.end_date = end_date_new
                        student_course.save()
                        return redirect('web:detail_school_student_user', pk=queryset.ref_student.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)

                else:
                    form = StudentProfileHasCourseForm(
                        instance=queryset, logged_in_user=logged_in_user)

                template_name = 'admin/master/student/edit_student_course.html'
                kwvars = {
                    'queryset': queryset,
                    'form': form,
                    'cdate': current_day,
                    'pdate': previous_day
                }
                return render(request, template_name, kwvars)
            else:
                print("=====================================")
                raise_permission_denied = True
        except StudentProfileHasCourse.DoesNotExist:
            print("===================================== except")
            raise_permission_denied = True
    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            queryset = StudentProfileHasCourse.objects.get(id=pk)
            if queryset.ref_student.ref_school.id:
                data = request.POST.dict()
                form = StudentProfileHasCourseForm(
                    instance=queryset, logged_in_user=queryset.ref_student.ref_school.id)
                if request.method == 'POST':
                    form = StudentProfileHasCourseForm(
                        request.POST, instance=queryset, logged_in_user=queryset.ref_student.ref_school.id)
                    if form.is_valid():
                        student_course = form.save(commit=False)
                        ref_course = data.get('ref_course')
                        study_period = data.get('study_period')
                        start_date = data.get('start_date')
                        if start_date and study_period:
                            day = (int(study_period) * 7)-3
                            date_1 = datetime.datetime.strptime(
                                start_date, "%Y-%m-%d")
                            date_2 = date_1 + datetime.timedelta(days=day)
                            end_date_new = date_2.strftime('%Y-%m-%d')
                        student_course.end_date = end_date_new
                        student_course.save()
                        return redirect('web:detail_school_student_user', pk=queryset.ref_student.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)

                else:
                    form = StudentProfileHasCourseForm(
                        instance=queryset, logged_in_user=queryset.ref_student.ref_school.id)

                template_name = 'admin/master/student/edit_student_course.html'
                kwvars = {
                    'queryset': queryset,
                    'form': form,
                    'cdate': current_day,
                    'pdate': previous_day
                }
                return render(request, template_name, kwvars)
            else:
                print("=====================================")
                raise_permission_denied = True
        except StudentProfileHasCourse.DoesNotExist:
            print("===================================== except")
            raise_permission_denied = True
    else:
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.add_schoolstudentuserprofile'], raise_exception=True)
def create_student_course(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            student = SchoolStudentUserProfile.objects.get(id=pk)
            if logged_in_user == student.ref_school.id:
                student = SchoolStudentUserProfile.objects.filter(pk=pk)
                student = student.first()
                # print(student)

                context = {}
                form = StudentProfileHasCourseForm(
                    request.POST or None, logged_in_user=logged_in_user)
                data = request.POST.dict()
                if request.method == 'POST':
                    if form.is_valid():
                        student_course = form.save(commit=False)
                        ref_course = data.get('ref_course')
                        study_period = data.get('study_period')
                        start_date = data.get('start_date')
                        if StudentProfileHasCourse.objects.filter(ref_student=student, ref_course=ref_course).exists():
                            form.add_error('', 'This course  already exists')
                        else:
                            if start_date and study_period:
                                day = (int(study_period) * 7)-3
                                date_1 = datetime.datetime.strptime(
                                    start_date, "%Y-%m-%d")
                                date_2 = date_1 + datetime.timedelta(days=day)
                                end_date = date_2.strftime('%Y-%m-%d')
                            student_course.ref_student = student
                            student_course.end_date = end_date
                            student_course.save()
                            print("========Successfully add==========")
                            return redirect('web:detail_school_student_user', pk=pk)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                context['form'] = form
                context['student'] = pk
                context['cdate'] = current_day
                context['pdate'] = previous_day
                return render(request, 'admin/master/student/create_student_course.html', context)
            else:
                raise_permission_denied = True
        except:
            raise_permission_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:

        try:
            student = SchoolStudentUserProfile.objects.get(id=pk)

            if student.ref_school.id:

                student = SchoolStudentUserProfile.objects.filter(pk=pk)
                student = student.first()
                # print(student)

                context = {}
                form = StudentProfileHasCourseForm(
                    request.POST or None, logged_in_user=student.ref_school.id)
                data = request.POST.dict()
                if request.method == 'POST':
                    if form.is_valid():
                        student_course = form.save(commit=False)
                        ref_course = data.get('ref_course')
                        study_period = data.get('study_period')
                        start_date = data.get('start_date')
                        if StudentProfileHasCourse.objects.filter(ref_student=student, ref_course=ref_course).exists():
                            form.add_error('', 'This course  already exists')
                        else:
                            if start_date and study_period:
                                day = (int(study_period) * 7)-3
                                date_1 = datetime.datetime.strptime(
                                    start_date, "%Y-%m-%d")
                                date_2 = date_1 + datetime.timedelta(days=day)
                                end_date = date_2.strftime('%Y-%m-%d')
                            student_course.ref_student = student
                            student_course.end_date = end_date
                            student_course.save()
                            print("========Successfully add==========")
                            return redirect('web:detail_school_student_user', pk=pk)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                context['form'] = form
                context['student'] = pk
                context['cdate'] = current_day
                context['pdate'] = previous_day
                return render(request, 'admin/master/student/create_student_course.html', context)
            else:
                raise_permission_denied = True
        except:
            raise_permission_denied = True
    else:
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.delete_schoolstudentuserprofile'], raise_exception=True)
def delete_student_course(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        # print(logged_in_user)
        try:
            student_course = StudentProfileHasCourse.objects.get(id=pk)
            _id = student_course.ref_student.ref_school.id
            print(_id)
            print(logged_in_user)
            print(student_course)
            if logged_in_user == _id:
                print("===========")
                if request.method == 'POST':
                    pass
                    student_course.delete()
                    print("Delete Successfully")
                    return redirect('web:detail_school_student_user', pk=student_course.ref_student.id)
                return render(request, 'admin/master/student/delete_student_course.html', {'student_course': student_course})
            else:
                print("==============================auth error===========")
                raise_permission_denied = True

        except:
            print("==============================try error===========")
            raise_permission_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            student_course = StudentProfileHasCourse.objects.get(id=pk)
            _id = student_course.ref_student.ref_school.id

            if _id:
                print("===========")
                if request.method == 'POST':
                    pass
                    student_course.delete()
                    print("Delete Successfully")
                    return redirect('web:detail_school_student_user', pk=student_course.ref_student.id)
                return render(request, 'admin/master/student/delete_student_course.html', {'student_course': student_course})
            else:
                print("==============================auth error===========")
                raise_permission_denied = True

        except:
            print("==============================try error===========")
            raise_permission_denied = True

    else:
        print("==============================groups error===========")
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


@login_required
def create_student_accommodation(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        user_school_id = request.user.organizationuserprofile.ref_school.id
        try:
            student = SchoolStudentUserProfile.objects.get(id=pk)
            if user_school_id == student.ref_school.id:
                student = SchoolStudentUserProfile.objects.filter(pk=pk)
                student = student.first()
                # print(student)

                context = {}
                form = StudentProfileHasAccommodationForm(
                    request.POST or None, user_school_id=user_school_id)
                data = request.POST.dict()
                if request.method == 'POST':
                    if form.is_valid():
                        student_accommodation = form.save(commit=False)
                        ref_accommodation_room = data.get(
                            'ref_accommodation_room')
                        start_date = data.get('start_date')
                        end_date = data.get('end_date')

                        student_accommodation.ref_student = student
                        student_accommodation.save()
                        print("========Successfully add==========")
                        return redirect('web:detail_school_student_user', pk=pk)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                context['form'] = form
                context['student'] = student
                context['cdate'] = current_day
                context['pdate'] = previous_day
                return render(request, 'admin/master/student/create_student_accommodation.html', context)
            else:
                raise_permission_denied = True
        except:
            raise_permission_denied = True
    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            student = SchoolStudentUserProfile.objects.get(id=pk)
            if student.ref_school.id:
                student = SchoolStudentUserProfile.objects.filter(pk=pk)
                student = student.first()
                # print(student)

                context = {}
                form = StudentProfileHasAccommodationForm(
                    request.POST or None, user_school_id=student.ref_school.id)
                data = request.POST.dict()
                if request.method == 'POST':
                    if form.is_valid():
                        student_accommodation = form.save(commit=False)
                        ref_accommodation_room = data.get(
                            'ref_accommodation_room')
                        start_date = data.get('start_date')
                        end_date = data.get('end_date')

                        student_accommodation.ref_student = student
                        student_accommodation.save()
                        print("========Successfully add==========")
                        return redirect('web:detail_school_student_user', pk=pk)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                context['form'] = form
                context['student'] = student
                context['cdate'] = current_day
                context['pdate'] = previous_day
                return render(request, 'admin/master/student/create_student_accommodation.html', context)
            else:
                raise_permission_denied = True
        except:
            raise_permission_denied = True
    else:
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


@login_required
def update_student_accommodation(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        user_school_id = request.user.organizationuserprofile.ref_school.id

        try:
            queryset = StudentProfileHasAccommodation.objects.get(id=pk)
            # print(logged_in_user)
            print(queryset)
            if user_school_id == queryset.ref_student.ref_school.id:
                data = request.POST.dict()
                form = StudentProfileHasAccommodationForm(
                    instance=queryset, user_school_id=user_school_id)
                if request.method == 'POST':
                    form = StudentProfileHasAccommodationForm(
                        request.POST, instance=queryset, user_school_id=user_school_id)
                    if form.is_valid():
                        student_accommodation = form.save(commit=False)
                        ref_accommodation_room = data.get(
                            'ref_accommodation_room')
                        start_date = data.get('start_date')
                        end_date = data.get('end_date')
                        student_accommodation.save()
                        return redirect('web:detail_school_student_user', pk=queryset.ref_student.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)

                else:
                    form = StudentProfileHasAccommodationForm(
                        instance=queryset, user_school_id=user_school_id)

                template_name = 'admin/master/student/update_student_accommodation.html'
                kwvars = {
                    'queryset': queryset,
                    'form': form,
                    'cdate': current_day,
                    'pdate': previous_day
                }
                return render(request, template_name, kwvars)
            else:
                print("=====================================")
                raise_permission_denied = True
        except StudentProfileHasAccommodation.DoesNotExist:
            print("===================================== except")
            raise_permission_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            queryset = StudentProfileHasAccommodation.objects.get(id=pk)
            # print(logged_in_user)
            print(queryset)
            if queryset.ref_student.ref_school.id:
                data = request.POST.dict()
                form = StudentProfileHasAccommodationForm(
                    instance=queryset, user_school_id=queryset.ref_student.ref_school.id)
                if request.method == 'POST':
                    form = StudentProfileHasAccommodationForm(
                        request.POST, instance=queryset, user_school_id=queryset.ref_student.ref_school.id)
                    if form.is_valid():
                        student_accommodation = form.save(commit=False)
                        ref_accommodation_room = data.get(
                            'ref_accommodation_room')
                        start_date = data.get('start_date')
                        end_date = data.get('end_date')
                        student_accommodation.save()
                        return redirect('web:detail_school_student_user', pk=queryset.ref_student.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)

                else:
                    form = StudentProfileHasAccommodationForm(
                        instance=queryset, user_school_id=queryset.ref_student.ref_school.id)

                template_name = 'admin/master/student/update_student_accommodation.html'
                kwvars = {
                    'queryset': queryset,
                    'form': form,
                    'cdate': current_day,
                    'pdate': previous_day
                }
                return render(request, template_name, kwvars)
            else:
                print("=====================================")
                raise_permission_denied = True
        except StudentProfileHasAccommodation.DoesNotExist:
            print("===================================== except")
            raise_permission_denied = True
    else:
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


@login_required
def delete_student_accommodation(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        # print(logged_in_user)
        try:
            student_accommodation = StudentProfileHasAccommodation.objects.get(
                id=pk)
            _id = student_accommodation.ref_student.ref_school.id

            if logged_in_user == _id:
                print("===========")
                if request.method == 'POST':
                    pass
                    student_accommodation.delete()
                    print("Delete Successfully")
                    return redirect('web:detail_school_student_user', pk=student_accommodation.ref_student.id)
                return render(request, 'admin/master/student/delete_student_accommodation.html', {'student_accommodation': student_accommodation})
            else:
                print("==============================auth error===========")
                raise_permission_denied = True

        except:
            print("==============================try error===========")
            raise_permission_denied = True
    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            student_accommodation = StudentProfileHasAccommodation.objects.get(
                id=pk)
            _id = student_accommodation.ref_student.ref_school.id

            if _id:

                if request.method == 'POST':
                    student_accommodation.delete()
                    print("Delete Successfully")
                    return redirect('web:detail_school_student_user', pk=student_accommodation.ref_student.id)
                return render(request, 'admin/master/student/delete_student_accommodation.html', {'student_accommodation': student_accommodation})
            else:
                print("==============================auth error===========")
                raise_permission_denied = True

        except:
            print("==============================try error===========")
            raise_permission_denied = True

    else:
        print("==============================groups error===========")
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


@login_required
def create_student_service(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        user_school_id = request.user.organizationuserprofile.ref_school.id
        try:
            student = SchoolStudentUserProfile.objects.get(id=pk)
            if user_school_id == student.ref_school.id:
                student = SchoolStudentUserProfile.objects.filter(pk=pk)
                student = student.first()
                # print(student)

                context = {}
                form = StudentProfileHasServiceForm(
                    request.POST or None, user_school_id=user_school_id)
                data = request.POST.dict()
                if request.method == 'POST':
                    if form.is_valid():
                        student_service = form.save(commit=False)

                        student_service.ref_student = student
                        student_service.save()
                        print("========Successfully Add==========")
                        return redirect('web:detail_school_student_user', pk=pk)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                context['form'] = form
                context['student'] = student
                context['cdate'] = current_day
                context['pdate'] = previous_day
                return render(request, 'admin/master/student/create_student_service.html', context)
            else:
                raise_permission_denied = True
        except:
            raise_permission_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            student = SchoolStudentUserProfile.objects.get(id=pk)
            if student.ref_school.id:
                student = SchoolStudentUserProfile.objects.filter(pk=pk)
                student = student.first()
                # print(student)

                context = {}
                form = StudentProfileHasServiceForm(
                    request.POST or None, user_school_id=student.ref_school.id)
                data = request.POST.dict()
                if request.method == 'POST':
                    if form.is_valid():
                        student_service = form.save(commit=False)

                        student_service.ref_student = student
                        student_service.save()
                        print("========Successfully Add==========")
                        return redirect('web:detail_school_student_user', pk=pk)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                context['form'] = form
                context['student'] = student
                context['cdate'] = current_day
                context['pdate'] = previous_day
                return render(request, 'admin/master/student/create_student_service.html', context)
            else:
                raise_permission_denied = True
        except:
            raise_permission_denied = True
    
    else:
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


@login_required
def update_student_service(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        user_school_id = request.user.organizationuserprofile.ref_school.id

        try:
            queryset = StudentProfileHasService.objects.get(id=pk)
            # print(logged_in_user)
            print(queryset)
            if user_school_id == queryset.ref_student.ref_school.id:
                data = request.POST.dict()
                form = StudentProfileHasServiceForm(
                    instance=queryset, user_school_id=user_school_id)
                if request.method == 'POST':
                    form = StudentProfileHasServiceForm(
                        request.POST, instance=queryset, user_school_id=user_school_id)
                    if form.is_valid():
                        student_service = form.save(commit=False)

                        student_service.save()
                        return redirect('web:detail_school_student_user', pk=queryset.ref_student.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)

                else:
                    form = StudentProfileHasServiceForm(
                        instance=queryset, user_school_id=user_school_id)

                template_name = 'admin/master/student/update_student_service.html'
                kwvars = {
                    'queryset': queryset,
                    'form': form,
                    'cdate': current_day,
                    'pdate': previous_day
                }
                return render(request, template_name, kwvars)
            else:
                print("=====================================")
                raise_permission_denied = True
        except StudentProfileHasServiceForm.DoesNotExist:
            print("===================================== except")
            raise_permission_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            queryset = StudentProfileHasServiceForm.objects.get(id=pk)
            # print(logged_in_user)
            print(queryset)
            if queryset.ref_student.ref_school.id:
                data = request.POST.dict()
                form = StudentProfileHasServiceForm(
                    instance=queryset, user_school_id=queryset.ref_student.ref_school.id)
                if request.method == 'POST':
                    form = StudentProfileHasServiceForm(
                        request.POST, instance=queryset, user_school_id=queryset.ref_student.ref_school.id)
                    if form.is_valid():
                        student_accommodation = form.save(commit=False)

                        student_accommodation.save()
                        return redirect('web:detail_school_student_user', pk=queryset.ref_student.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)

                else:
                    form = StudentProfileHasServiceForm(
                        instance=queryset, user_school_id=queryset.ref_student.ref_school.id)

                template_name = 'admin/master/student/update_student_service.html'
                kwvars = {
                    'queryset': queryset,
                    'form': form,
                    'cdate': current_day,
                    'pdate': previous_day
                }
                return render(request, template_name, kwvars)
            else:
                print("=====================================")
                raise_permission_denied = True
        except StudentProfileHasServiceForm.DoesNotExist:
            print("===================================== except")
            raise_permission_denied = True
    else:
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


@login_required
def delete_student_service(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        # print(logged_in_user)
        try:
            student_service = StudentProfileHasService.objects.get(
                id=pk)
            _id = student_service.ref_student.ref_school.id

            if logged_in_user == _id:
                print("===========")
                if request.method == 'POST':
                    pass
                    student_service.delete()
                    print("Delete Successfully")
                    return redirect('web:detail_school_student_user', pk=student_service.ref_student.id)
                return render(request, 'admin/master/student/delete_student_service.html', {'student_service': student_service})
            else:
                print("==============================auth error===========")
                raise_permission_denied = True

        except:
            print("==============================try error===========")
            raise_permission_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            student_service = StudentProfileHasService.objects.get(
                id=pk)
            _id = student_service.ref_student.ref_school.id

            if _id:

                if request.method == 'POST':
                    student_service.delete()
                    print("Delete Successfully")
                    return redirect('web:detail_school_student_user', pk=student_service.ref_student.id)
                return render(request, 'admin/master/student/delete_student_service.html', {'student_service': student_service})
            else:
                print("==============================auth error===========")
                raise_permission_denied = True

        except:
            print("==============================try error===========")
            raise_permission_denied = True

    else:
        print("==============================groups error===========")
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


def get_school_service(request):
    service_type = request.GET.get('service_type')
    school_id = request.GET.get('school_id')

    if not service_type and not school_id:
        return render(request, 'admin/master/school_service_dropdown_list_options.html', {'services': []})

    services = SchoolService.objects.filter(
        ref_school__pk=school_id, service_type=service_type)

    return render(request, 'admin/master/school_service_dropdown_list_options.html', {'services': services})


def get_installment_details(request):
    class_id = request.GET.get('class_id')
    installment_type = request.GET.get('installment_type')
    school_id = request.GET.get('school_id')
    application_id = request.GET.get('application_id')

    context = {}

    if installment_type and school_id and class_id and application_id:

        application = get_object_or_404(Application, pk=application_id)

        installment = get_object_or_404(SchoolClassInstallment,
                                        ref_class__pk=class_id, type=installment_type)

        net_amount = application.ap_grand_total + \
            (application.ap_grand_total * installment.charges) / 100

        divided_by = 0
        if installment_type == 'Per Week':
            divided_by = 1
        elif installment_type == 'Per Month':
            divided_by = 4
        elif installment_type == 'Three Times':
            divided_by = int(application.ap_study_period/3)

        total_installments = int(application.ap_study_period / divided_by)
        installments_amount = round(net_amount / total_installments, 2)

        context['application'] = application
        context['net_amount'] = round(net_amount, 2)
        context['installment'] = installment
        context['installments_amount'] = installments_amount
        context['total_installments'] = total_installments

        return render(request, 'admin/master/installment_details.html', context=context)

    return render(request, 'admin/master/installment_details.html', {})
