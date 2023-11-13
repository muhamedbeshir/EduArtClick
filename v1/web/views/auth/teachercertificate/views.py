from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Group

from v1.db.models import *
from .forms import *

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError

current_day = date.today()
previous_day = date.today() - timedelta(days=1)


@login_required
@permission_required(['db.add_certificateteacher'], raise_exception=True)
def create_certificate_teacher_by_school(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            profile = TeacherUserProfile.objects.get(id=pk)
            _id = profile.ref_school.id

            if logged_in_user == _id:
                data = request.POST.dict()
                form = CertificateTeacherForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        certificate = form.save(commit=False)
                        name = data.get('name')
                        code = data.get('code')
                        date = data.get('date')
                        try:
                            certificate.ref_teacher_user_profile = profile
                            certificate.save()
                            print("Successfully add data")
                            return redirect('web:school_teacher_detail', pk=profile.id)
                        except IntegrityError:
                            error = f"Code: '{str(code).upper()}' already exist."
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'auth/teachercertificate/create_certificate_teacher_by_school.html', {'teacher': pk, 'form': form, 'cday': current_day})
            else:
                print("============Error===================")
                raise_permision_denied = True
        except User.DoesNotExist:
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            profile = TeacherUserProfile.objects.get(id=pk)
            _id = profile.ref_school.id

            if _id:
                data = request.POST.dict()
                form = CertificateTeacherForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        certificate = form.save(commit=False)
                        name = data.get('name')
                        code = data.get('code')
                        date = data.get('date')
                        try:
                            certificate.ref_teacher_user_profile = profile
                            certificate.save()
                            print("Successfully add data")
                            return redirect('web:school_teacher_detail', pk=profile.id)
                        except IntegrityError:
                            error = f"Code: '{str(code).upper()}' already exist."
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'auth/teachercertificate/create_certificate_teacher_by_school.html', {'teacher': pk, 'form': form, 'cday': current_day})
            else:
                print("============Error===================")
                raise_permision_denied = True
        except User.DoesNotExist:
            raise_permision_denied = True
    else:
        raise_permision_denied = True
    
    if raise_permision_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.change_certificateteacher'], raise_exception=True)
def edit_certificate_teacher_by_school(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            queryset = CertificateTeacher.objects.get(id=pk)
            _id = queryset.ref_teacher_user_profile.ref_school.id

            if logged_in_user == _id:
                data = request.POST.dict()
                form = CertificateTeacherForm(instance=queryset)
                if request.method == 'POST':
                    form = CertificateTeacherForm(
                        request.POST, instance=queryset)
                    if form.is_valid():
                        try:
                            form.save()
                            print("Successfully update data")
                            return redirect('web:school_teacher_detail', pk=queryset.ref_teacher_user_profile.id)
                        except IntegrityError:
                            error = "Data with this code is already exist."
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = CertificateTeacherForm(instance=queryset)
                template_name = 'auth/teachercertificate/edit_certificate_teacher_by_school.html'
                kwvars = {
                    'certificate': queryset,
                    'form': form,
                    'cdate': current_day,
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except CertificateTeacher.DoesNotExist:
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            queryset = CertificateTeacher.objects.get(id=pk)
            _id = queryset.ref_teacher_user_profile.ref_school.id

            if _id:
                data = request.POST.dict()
                form = CertificateTeacherForm(instance=queryset)
                if request.method == 'POST':
                    form = CertificateTeacherForm(
                        request.POST, instance=queryset)
                    if form.is_valid():
                        try:
                            form.save()
                            print("Successfully update data")
                            return redirect('web:school_teacher_detail', pk=queryset.ref_teacher_user_profile.id)
                        except IntegrityError:
                            error = "Data with this code is already exist."
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = CertificateTeacherForm(instance=queryset)
                template_name = 'auth/teachercertificate/edit_certificate_teacher_by_school.html'
                kwvars = {
                    'certificate': queryset,
                    'form': form,
                    'cdate': current_day,
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except CertificateTeacher.DoesNotExist:
            raise_permision_denied = True
    else:
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.delete_certificateteacher'], raise_exception=True)
def delete_certificate_teacher_by_school(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        print(logged_in_user)
        try:
            certificate = CertificateTeacher.objects.get(id=pk)
            _id = certificate.ref_teacher_user_profile.ref_school.id

            if logged_in_user == _id:
                if request.method == 'POST':
                    certificate.delete()
                    print("Delete Successfully")
                    return redirect('web:school_teacher_detail', pk=certificate.ref_teacher_user_profile.id)
                else:
                    pass
                return render(request, 'auth/teachercertificate/delete_certificate_teacher_by_school.html', {'address': address})
            else:
                print("==============================auth error===========")
                raise_permision_denied = True

        except:
            print("==============================try error===========")
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            certificate = CertificateTeacher.objects.get(id=pk)
            _id = certificate.ref_teacher_user_profile.ref_school.id

            if _id:
                if request.method == 'POST':
                    certificate.delete()
                    print("Delete Successfully")
                    return redirect('web:school_teacher_detail', pk=certificate.ref_teacher_user_profile.id)
                else:
                    pass
                return render(request, 'auth/teachercertificate/delete_certificate_teacher_by_school.html', {'address': address})
            else:
                print("==============================auth error===========")
                raise_permision_denied = True

        except:
            print("==============================try error===========")
            raise_permision_denied = True
    else:
        print("==============================groups error===========")
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()
