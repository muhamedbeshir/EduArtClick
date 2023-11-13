from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Max, Min
from django.core.exceptions import PermissionDenied
from v1.db.models import TeacherUserProfile, CertificateTeacher, UserAddress, UserContact
from v1.web.utils import CHECK_USER_PERMISSION

from .forms import *

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError


current_day = date.today()
previous_day = date.today() - timedelta(days=1)


class DetailTeacher(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ('db.view_teacheruserprofile',)
    model = TeacherUserProfile
    context_object_name = 'teacher'
    template_name = 'admin/master/teacher/teacher_detail.html'

    def get_user(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        user = self.get_user()
        if user.groups.filter(name='school').exists():
            logged_in_user = user.organizationuserprofile.ref_school.id
            try:
                teacher_id = self.kwargs.get('pk', None)
                teacher = TeacherUserProfile.objects.get(id=teacher_id)
                if logged_in_user == teacher.ref_school.id:
                    context = super(
                        DetailTeacher, self).get_context_data(**kwargs)
                    queryset = TeacherUserProfile.objects.filter(
                        pk=teacher_id, ref_school=logged_in_user)
                    context["certificateteacher"] = CertificateTeacher.objects.filter(
                        ref_teacher_user_profile=teacher.id)
                    context["address"] = UserAddress.objects.filter(
                        ref_user=teacher.ref_user.id)
                    context["contact"] = UserContact.objects.filter(
                        ref_user=teacher.ref_user.id)
                    return context
                else:
                    context = super(
                        DetailTeacher, self).get_context_data(**kwargs)
                    context["permission"] = "permission"
                    return context
            except:
                context = super(DetailTeacher, self).get_context_data(**kwargs)
                context["permission"] = "permission"
                return context
        elif user.groups.filter(name='admin').exists() or user.is_superuser:
            # print("===========================================")
            try:
                teacher_id = self.kwargs.get('pk', None)
                teacher = TeacherUserProfile.objects.get(id=teacher_id)
                print("=================================teacher_id")
                if teacher.ref_school.id:
                    context = super(
                        DetailTeacher, self).get_context_data(**kwargs)
                    print(
                        "=============================================== if ---------------")
                    queryset = TeacherUserProfile.objects.filter(
                        pk=teacher_id, ref_school=teacher.ref_school.id)
                    context["certificateteacher"] = CertificateTeacher.objects.filter(
                        ref_teacher_user_profile=teacher.id)
                    context["address"] = UserAddress.objects.filter(
                        ref_user=teacher.ref_user.id)
                    context["contact"] = UserContact.objects.filter(
                        ref_user=teacher.ref_user.id)
                    return context
                else:
                    context = super(
                        DetailTeacher, self).get_context_data(**kwargs)
                    context["permission"] = "permission"
                    return context
            except:
                context = super(DetailTeacher, self).get_context_data(**kwargs)
                context["permission"] = "permission"
                return context
        else:
            context = super(DetailTeacher, self).get_context_data(**kwargs)
            context["permission"] = "permission"
            return context


@login_required
@permission_required(['db.change_teacheruserprofile'], raise_exception=True)
def update_teacher(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        # print("===============================================")
        # print(logged_in_user)
        try:
            queryset = TeacherUserProfile.objects.get(id=pk)

            if logged_in_user == queryset.ref_school.id:

                data = request.POST.dict()
                form = UpdateSchoolTeacherForm(instance=queryset)
                if request.method == 'POST':
                    form = UpdateSchoolTeacherForm(
                        request.POST, instance=queryset)
                    if form.is_valid():
                        teacher = form.save(commit=False)
                        teacher.save()
                        print("Successfully edit data")
                        return redirect('web:deatil_school', pk=logged_in_user)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                        print(form.errors)
                else:
                    form = UpdateSchoolTeacherForm(instance=queryset)

                template_name = 'admin/master/teacher/edit_teacher.html'
                kwvars = {
                    'teacher': queryset,
                    'form': form,
                    'cdate': current_day, 'pdate': previous_day
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except:
            raise_permision_denied = True
    
    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            queryset = TeacherUserProfile.objects.get(id=pk)

            if queryset.ref_school.id:

                data = request.POST.dict()
                form = UpdateSchoolTeacherForm(instance=queryset)
                if request.method == 'POST':
                    form = UpdateSchoolTeacherForm(
                        request.POST, instance=queryset)
                    if form.is_valid():
                        teacher = form.save(commit=False)
                        teacher.save()
                        print("Successfully edit data")
                        return redirect('web:deatil_school', pk=queryset.ref_school.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                        print(form.errors)
                else:
                    form = UpdateSchoolTeacherForm(instance=queryset)

                template_name = 'admin/master/teacher/edit_teacher.html'
                kwvars = {
                    'teacher': queryset,
                    'form': form,
                    'cdate': current_day, 'pdate': previous_day
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except:
            raise_permision_denied = True
    else:
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()
