import json
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.http import HttpResponse
import random
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.db import transaction
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage, send_mail
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.views.generic import ListView, CreateView, UpdateView
import re

from django.template import RequestContext

from django.contrib.auth.models import User, Group

import datetime
from datetime import date, timedelta
import phonenumbers
from v1.db.master.school_accommodation_service import SchoolAccommodationService
from v1.db.master.school_class import SchoolClass
from v1.db.master.school_course_level import SchoolCourseLevel
from v1.db.master.school_service import SchoolService
from v1.db.models import Application, Organization, UserProfile, StudentUserProfile, AggentUserProfile, AuthForgetPasswordToken

from django.views.generic import TemplateView, DeleteView
from v1.db.user.student_profile_has_accommodation import StudentProfileHasAccommodation

from v1.db.user.student_profile_has_course import StudentProfileHasCourse
from v1.db.user.student_profile_has_service import StudentProfileHasService

from .forms import *
from .serializers import *

from .token import *


current_day = date.today()
previous_day = date.today() - timedelta(days=1)


class RegistrationPage(TemplateView):
    template_name = 'auth/registration_page.html'


class UserCraetePage(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('auth.view_user')
    template_name = 'auth/dashboard/user_craete_page.html'

    def get_context_data(self, **kwargs):
        context = super(UserCraetePage, self).get_context_data(**kwargs)
        student = StudentUserProfile.objects.all()
        active_student = StudentUserProfile.objects.filter(
            ref_user__is_active=True)
        deactive_student = StudentUserProfile.objects.filter(
            ref_user__is_active=False)
        aggent = AggentUserProfile.objects.all()
        active_aggent = AggentUserProfile.objects.filter(
            ref_user__is_active=True)
        deactive_aggent = AggentUserProfile.objects.filter(
            ref_user__is_active=False)
        staff = UserProfile.objects.filter(
            ref_user__groups__name__in=['staff'])
        active_staff = UserProfile.objects.filter(
            ref_user__is_active=True, ref_user__groups__name__in=['staff'])
        deactive_staff = UserProfile.objects.filter(
            ref_user__is_active=False, ref_user__groups__name__in=['staff'])
        admin = UserProfile.objects.filter(
            ref_user__groups__name__in=['admin'])
        active_admin = UserProfile.objects.filter(
            ref_user__is_active=True, ref_user__groups__name__in=['admin'])
        deactive_admin = UserProfile.objects.filter(
            ref_user__is_active=False, ref_user__groups__name__in=['admin'])
        organization = OrganizationUserProfile.objects.filter(
            ref_user__groups__name__in=['organization'])
        active_organization = OrganizationUserProfile.objects.filter(
            ref_user__is_active=True, ref_user__groups__name__in=['organization'])
        deactive_organization = OrganizationUserProfile.objects.filter(
            ref_user__is_active=False, ref_user__groups__name__in=['organization'])
        school = OrganizationUserProfile.objects.filter(
            ref_user__groups__name__in=['school'])
        active_school = OrganizationUserProfile.objects.filter(
            ref_user__is_active=True, ref_user__groups__name__in=['school'])
        deactive_school = OrganizationUserProfile.objects.filter(
            ref_user__is_active=False, ref_user__groups__name__in=['school'])
        context['student'] = student
        context['student_total'] = len(list(student))
        context['active_student_total'] = len(list(active_student))
        context['deactive_student_total'] = len(list(deactive_student))
        context['aggent'] = aggent
        context['aggent_total'] = len(list(aggent))
        context['active_aggent_total'] = len(list(active_aggent))
        context['deactive_aggent_total'] = len(list(deactive_aggent))
        context['staff'] = staff
        context['staff_total'] = len(list(staff))
        context['active_staff_total'] = len(list(active_staff))
        context['deactive_staff_total'] = len(list(deactive_staff))
        context['admin'] = admin
        context['admin_total'] = len(list(admin))
        context['active_admin_total'] = len(list(active_admin))
        context['deactive_admin_total'] = len(list(deactive_admin))
        context['organization'] = organization
        context['organization_total'] = len(list(organization))
        context['active_organization'] = len(list(active_organization))
        context['deactive_organization'] = len(list(deactive_organization))
        context['school'] = school
        context['school_total'] = len(list(school))
        context['active_school'] = len(list(active_school))
        context['deactive_school'] = len(list(deactive_school))
        return context


@login_required
@permission_required(['db.add_studentuserprofile'], raise_exception=True)
def create_student_user(request):
    data = request.POST.dict()
    form = StudentSignUpForm(data or None, request.FILES or None)

    if request.method == 'POST':

        if form.is_valid():
            profile = form.save(commit=False)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')

            if User.objects.filter(email=email).exists():
                form.add_error('', 'User already exists')

            else:

                user = User.objects.create_user(
                    username=email, email=email, first_name=first_name, last_name=last_name)
                password = get_random_string(128)
                user.is_active = False
                user.set_password(password)
                user.save()
                ctoken = get_random_string(192)
                pwd_reset_data = {"user": user.id, "token": ctoken}
                pwd_reset_serializer = AuthForgetPasswordSerializer(
                    data=pwd_reset_data)

                if pwd_reset_serializer.is_valid():
                    pwd_reset_serializer.save()

                    try:
                        message = render_to_string('auth/acc_active_email.html', {
                            "email": user.email,
                            'user': user,
                            'domain': request.headers['Host'],
                            'site_name': 'Interface',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': pwd_reset_serializer.data["token"],
                            'protocol': 'http',
                        })
                        subject = 'Activate your account.'
                        to_email = user.email
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                  to_email], fail_silently=False)
                        print("Mail send")
                    except Exception as e:
                        print(e)

                profile.ref_user = user
                group = Group.objects.get(name='student')
                profile.save()
                group.user_set.add(user)
                return redirect('web:create_user_page')
        else:
            form.add_error('', 'Form is not valid')

    return render(request, 'auth/dashboard/create_student_user.html', {'form': form})


@login_required
@permission_required(['db.change_studentuserprofile'], raise_exception=True)
def edit_student_user(request, pk):
    data = request.POST.dict()
    form = EditStudentSignUpForm(data or None, request.FILES or None)
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':

        if form.is_valid():
            first_name = data.get('first_name')
            last_name = data.get('last_name')

            student_user_profile = get_object_or_404(
                StudentUserProfile, ref_user=user)

            user.first_name = first_name
            user.last_name = last_name

            student_user_profile.first_name = first_name
            student_user_profile.last_name = last_name

            user.save()
            student_user_profile.save()

            return redirect('web:create_user_page')
        else:
            form.add_error('', 'Form is not valid')
    elif request.method == 'GET':
        form = EditStudentSignUpForm({
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        return render(request, 'auth/dashboard/edit_student_user.html', {'form': form})


@login_required
@permission_required(['db.add_aggentuserprofile'], raise_exception=True)
def create_agent_user(request):
    data = request.POST.dict()
    form = AgentSignUpForm(data or None, request.FILES or None)

    if request.method == 'POST':

        if form.is_valid():
            profile = form.save(commit=False)
            company_name = data.get('company_name')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')

            if User.objects.filter(email=email).exists():
                form.add_error('', 'User already exists')

            else:

                user = User.objects.create_user(
                    username=email, email=email, first_name=first_name, last_name=last_name)
                password = get_random_string(128)
                user.is_active = False
                user.set_password(password)
                user.save()
                ctoken = get_random_string(192)
                pwd_reset_data = {"user": user.id, "token": ctoken}
                pwd_reset_serializer = AuthForgetPasswordSerializer(
                    data=pwd_reset_data)

                if pwd_reset_serializer.is_valid():
                    pwd_reset_serializer.save()

                    try:
                        message = render_to_string('auth/acc_active_email.html', {
                            "email": user.email,
                            'user': user,
                            'domain': request.headers['Host'],
                            'site_name': 'Interface',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': pwd_reset_serializer.data["token"],
                            'protocol': 'http',
                        })
                        subject = 'Activate your account.'
                        to_email = user.email
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                  to_email], fail_silently=False)
                        print("Mail send")
                    except Exception as e:
                        print(e)

                profile.ref_user = user
                group = Group.objects.get(name='aggent')
                profile.save()
                group.user_set.add(user)

                return redirect('web:create_user_page')

                # return redirect(redirect_url)
        else:
            form.add_error('', 'Form is not valid')

    return render(request, 'auth/dashboard/create_agent_user.html', {'form': form})


@login_required
@permission_required(['db.change_aggentuserprofile'], raise_exception=True)
def edit_agent_user(request, pk):
    data = request.POST.dict()
    form = EditAgentSignUpForm(data or None, request.FILES or None)
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':

        if form.is_valid():
            company_name = data.get('company_name')
            first_name = data.get('first_name')
            last_name = data.get('last_name')

            agent_user = get_object_or_404(AggentUserProfile, ref_user=user)

            user.first_name = first_name
            user.last_name = last_name

            agent_user.company_name = company_name
            agent_user.first_name = first_name
            agent_user.last_name = last_name

            user.save()
            agent_user.save()

            return redirect('web:create_user_page')
        else:
            form.add_error('', 'Form is not valid')
    elif request.method == 'GET':
        agent_user = get_object_or_404(AggentUserProfile, ref_user=user)
        form = EditAgentSignUpForm({
            'company_name': agent_user.company_name,
            'first_name': agent_user.first_name,
            'last_name': agent_user.last_name,
        })
        return render(request, 'auth/dashboard/edit_agent_user.html', {'form': form})


@login_required
@permission_required(['db.add_userprofile'], raise_exception=True)
def create_staff_user(request):
    data = request.POST.dict()
    form = SignUpForm(data or None, request.FILES or None)

    if request.method == 'POST':

        if form.is_valid():
            profile = form.save(commit=False)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')

            if User.objects.filter(email=email).exists():
                form.add_error('', 'User already exists')
                print("User already exists")

            else:

                user = User.objects.create_user(
                    username=email, email=email, first_name=first_name, last_name=last_name)
                password = get_random_string(128)
                user.is_active = False
                user.set_password(password)
                user.save()
                ctoken = get_random_string(192)
                pwd_reset_data = {"user": user.id, "token": ctoken}
                pwd_reset_serializer = AuthForgetPasswordSerializer(
                    data=pwd_reset_data)

                if pwd_reset_serializer.is_valid():
                    pwd_reset_serializer.save()
                    # print("Token================================================")
                    # print(pwd_reset_serializer.data["token"])

                    try:
                        message = render_to_string('auth/acc_active_email.html', {
                            "email": user.email,
                            'user': user,
                            'domain': request.headers['Host'],
                            'site_name': 'Interface',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': pwd_reset_serializer.data["token"],
                            'protocol': 'http',
                        })
                        # print(message)
                        subject = 'Activate your account.'
                        to_email = user.email
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                  to_email], fail_silently=False)
                        print("Mail send")
                    except Exception as e:
                        print(e)

                profile.ref_user = user
                group = Group.objects.get(name='staff')
                profile.save()
                group.user_set.add(user)

                return redirect('web:create_user_page')

                # return redirect(redirect_url)
        else:
            form.add_error('', 'Form is not valid')

    return render(request, 'auth/dashboard/create_staff_user.html', {'form': form})


@login_required
@permission_required(['db.change_userprofile'], raise_exception=True)
def edit_staff_user(request, pk):
    data = request.POST.dict()
    form = EditSignUpForm(data or None, request.FILES or None)
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':

        if form.is_valid():
            first_name = data.get('first_name')
            last_name = data.get('last_name')

            staff_user = get_object_or_404(UserProfile, ref_user=user)

            user.first_name = first_name
            user.last_name = last_name

            staff_user.first_name = first_name
            staff_user.last_name = last_name

            user.save()
            staff_user.save()

            return redirect('web:create_user_page')
        else:
            form.add_error('', 'Form is not valid')
    elif request.method == 'GET':
        form = EditSignUpForm({
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        return render(request, 'auth/dashboard/edit_staff_user.html', {'form': form})


@login_required
@permission_required(['db.add_userprofile'], raise_exception=True)
def create_admin_user(request):
    data = request.POST.dict()
    form = SignUpForm(data or None, request.FILES or None)

    if request.method == 'POST':

        if form.is_valid():
            profile = form.save(commit=False)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')

            if User.objects.filter(email=email).exists():
                form.add_error('', 'User already exists')
                print("User already exists")

            else:

                user = User.objects.create_user(
                    username=email, email=email, first_name=first_name, last_name=last_name)
                password = get_random_string(128)
                user.is_active = False
                user.set_password(password)
                user.save()
                ctoken = get_random_string(192)
                pwd_reset_data = {"user": user.id, "token": ctoken}
                pwd_reset_serializer = AuthForgetPasswordSerializer(
                    data=pwd_reset_data)

                if pwd_reset_serializer.is_valid():
                    pwd_reset_serializer.save()
                    # print("Token================================================")
                    # print(pwd_reset_serializer.data["token"])

                    try:
                        message = render_to_string('auth/acc_active_email.html', {
                            "email": user.email,
                            'user': user,
                            'domain': request.headers['Host'],
                            'site_name': 'Interface',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': pwd_reset_serializer.data["token"],
                            'protocol': 'http',
                        })
                        # print(message)
                        subject = 'Activate your account.'
                        to_email = user.email
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                  to_email], fail_silently=False)
                        print("Mail send")
                    except Exception as e:
                        print(e)

                profile.ref_user = user
                group = Group.objects.get(name='admin')
                profile.save()
                group.user_set.add(user)

                return redirect('web:create_user_page')

                # return redirect(redirect_url)
        else:
            form.add_error('', 'Form is not valid')

    return render(request, 'auth/dashboard/create_admin_user.html', {'form': form})


@login_required
@permission_required(['db.change_userprofile'], raise_exception=True)
def edit_admin_user(request, pk):
    data = request.POST.dict()
    form = EditSignUpForm(data or None, request.FILES or None)
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':

        if form.is_valid():
            first_name = data.get('first_name')
            last_name = data.get('last_name')

            staff_user = get_object_or_404(UserProfile, ref_user=user)

            user.first_name = first_name
            user.last_name = last_name

            staff_user.first_name = first_name
            staff_user.last_name = last_name

            user.save()
            staff_user.save()

            return redirect('web:create_user_page')
        else:
            form.add_error('', 'Form is not valid')
    elif request.method == 'GET':
        form = EditSignUpForm({
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        return render(request, 'auth/dashboard/edit_admin_user.html', {'form': form})


@login_required
@permission_required(['db.add_organizationuserprofile'], raise_exception=True)
def create_organization_user(request):
    data = request.POST.dict()
    form = OrganizationSignUpForm(data or None, request.FILES or None)

    if request.method == 'POST':

        if form.is_valid():
            profile = form.save(commit=False)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')

            if User.objects.filter(email=email).exists():
                form.add_error('', 'User already exists')
                print("User already exists")

            else:

                user = User.objects.create_user(
                    username=email, email=email, first_name=first_name, last_name=last_name)
                password = get_random_string(128)
                user.is_active = False
                user.set_password(password)
                user.save()
                ctoken = get_random_string(192)
                pwd_reset_data = {"user": user.id, "token": ctoken}
                pwd_reset_serializer = AuthForgetPasswordSerializer(
                    data=pwd_reset_data)

                if pwd_reset_serializer.is_valid():
                    pwd_reset_serializer.save()
                    # print("Token================================================")
                    # print(pwd_reset_serializer.data["token"])

                    try:
                        message = render_to_string('auth/acc_active_email.html', {
                            "email": user.email,
                            'user': user,
                            'domain': request.headers['Host'],
                            'site_name': 'Interface',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': pwd_reset_serializer.data["token"],
                            'protocol': 'http',
                        })
                        # print(message)
                        subject = 'Activate your account.'
                        to_email = user.email
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                  to_email], fail_silently=False)
                        print("Mail send")
                    except Exception as e:
                        print(e)

                profile.ref_user = user
                group = Group.objects.get(name='organization')
                profile.save()
                group.user_set.add(user)

                return redirect('web:create_user_page')

                # return redirect(redirect_url)
        else:
            form.add_error('', 'Form is not valid')

    return render(request, 'auth/dashboard/create_organization_user.html', {'form': form})


@login_required
@permission_required(['db.change_organizationuserprofile'], raise_exception=True)
def edit_organization_user(request, pk):
    data = request.POST.dict()
    form = EditOrganizationSignUpForm(data or None, request.FILES or None)
    user = get_object_or_404(User, pk=pk)
    org_user = get_object_or_404(OrganizationUserProfile, ref_user=user)

    if request.method == 'POST':

        if form.is_valid():
            ref_organization = data.get('ref_organization')
            first_name = data.get('first_name')
            last_name = data.get('last_name')

            organization = get_object_or_404(Organization, pk=ref_organization)

            user.first_name = first_name
            user.last_name = last_name

            org_user.ref_organization = organization
            org_user.first_name = first_name
            org_user.last_name = last_name

            user.save()
            org_user.save()

            return redirect('web:create_user_page')
        else:
            form.add_error('', 'Form is not valid')
    elif request.method == 'GET':
        form = EditOrganizationSignUpForm({
            'ref_organization': org_user.ref_organization,
            'first_name': org_user.first_name,
            'last_name': org_user.last_name,
        })
        return render(request, 'auth/dashboard/edit_organization_user.html', {'form': form})


@login_required
@permission_required(['db.add_organizationuserprofile'], raise_exception=True)
def create_school_user(request):
    data = request.POST.dict()
    form = SchoolSignUpForm(data or None, request.FILES or None)
    context = {
        'form': form
    }
    
    # Only for organization user
    if not request.user.is_superuser:
        if request.user.groups.all().first().name == 'organization':
            context['organization'] = request.user.organizationuserprofile.ref_organization


    if request.method == 'POST':

        if form.is_valid():
            profile = form.save(commit=False)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')

            if User.objects.filter(email=email).exists():
                form.add_error('', 'User already exists')
                print("User already exists")

            else:

                user = User.objects.create_user(
                    username=email, email=email, first_name=first_name, last_name=last_name)
                password = get_random_string(128)
                user.is_active = False
                user.set_password(password)
                user.save()
                ctoken = get_random_string(192)
                pwd_reset_data = {"user": user.id, "token": ctoken}
                pwd_reset_serializer = AuthForgetPasswordSerializer(
                    data=pwd_reset_data)

                if pwd_reset_serializer.is_valid():
                    pwd_reset_serializer.save()
                    # print("Token================================================")
                    # print(pwd_reset_serializer.data["token"])

                    try:
                        message = render_to_string('auth/acc_active_email.html', {
                            "email": user.email,
                            'user': user,
                            'domain': request.headers['Host'],
                            'site_name': 'Interface',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': pwd_reset_serializer.data["token"],
                            'protocol': 'http',
                        })
                        # print(message)
                        subject = 'Activate your account.'
                        to_email = user.email
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                  to_email], fail_silently=False)
                        print("Mail send")
                    except Exception as e:
                        print(e)

                profile.ref_user = user
                group = Group.objects.get(name='school')
                profile.save()
                group.user_set.add(user)

                if context['organization']:
                    return redirect(reverse("web:organization_school_user_list", kwargs={"pk": request.user.organizationuserprofile.pk}))

                return redirect('web:create_user_page')

                # return redirect(redirect_url)
        else:
            form.add_error('', 'Form is not valid')


    # Only for organization user
    if not request.user.is_superuser:
        if request.user.groups.all().first().name == 'organization':
            return render(request, 'auth/dashboard/create_school_user_org.html', context)

    return render(request, 'auth/dashboard/create_school_user.html', context)


@login_required
@permission_required(['db.change_organizationuserprofile'], raise_exception=True)
def edit_school_user(request, pk):
    data = request.POST.dict()
    form = EditSchoolSignUpForm(data or None, request.FILES or None)
    user = get_object_or_404(User, pk=pk)
    org_user = get_object_or_404(OrganizationUserProfile, ref_user=user)

    if request.method == 'POST':

        if form.is_valid():
            ref_organization = data.get('ref_organization')
            ref_school = data.get('ref_school')
            first_name = data.get('first_name')
            last_name = data.get('last_name')

            organization = get_object_or_404(Organization, pk=ref_organization)
            school = get_object_or_404(School, pk=ref_school)

            user.first_name = first_name
            user.last_name = last_name

            org_user.ref_organization = organization
            org_user.ref_school = school
            org_user.first_name = first_name
            org_user.last_name = last_name

            user.save()
            org_user.save()

            return redirect('web:create_user_page')
        else:
            form.add_error('', 'Form is not valid')
    elif request.method == 'GET':
        print(org_user.ref_school, '='*10)
        form = EditSchoolSignUpForm({
            'ref_organization': org_user.ref_organization,
            'ref_school': org_user.ref_school,
            'first_name': org_user.first_name,
            'last_name': org_user.last_name,
        })
        return render(request, 'auth/dashboard/edit_school_user.html', {'form': form})


@login_required
@permission_required(['db.add_organizationuserprofile'], raise_exception=True)
def create_school_user_by_organization(request, pk):
    profile = OrganizationUserProfile.objects.filter(pk=pk)
    profile = profile.first()
    school = School.objects.filter(
        ref_organization=profile.ref_organization.id)
    print(school)

    logged_in_user = request.user.organizationuserprofile.id
    if logged_in_user == profile.id:
        data = request.POST.dict()
        form = SchoolOrganizationSignUpForm(
            data or None, request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():
                profile_school = form.save(commit=False)
                ref_school = data.get('ref_school')
                first_name = data.get('first_name')
                last_name = data.get('last_name')
                email = data.get('email')
                if User.objects.filter(email=email).exists():
                    form.add_error('', 'User already exists')
                    print("User already exists")
                else:
                    user = User.objects.create_user(
                        username=email, email=email, first_name=first_name, last_name=last_name)
                    password = get_random_string(128)
                    user.is_active = False
                    user.set_password(password)
                    user.save()
                    ctoken = get_random_string(192)
                    pwd_reset_data = {"user": user.id, "token": ctoken}
                    pwd_reset_serializer = AuthForgetPasswordSerializer(
                        data=pwd_reset_data)

                    if pwd_reset_serializer.is_valid():
                        pwd_reset_serializer.save()
                        try:
                            message = render_to_string('auth/acc_active_email.html', {
                                "email": user.email,
                                'user': user,
                                'domain': request.headers['Host'],
                                'site_name': 'Interface',
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'token': pwd_reset_serializer.data["token"],
                                'protocol': 'http',
                            })
                            subject = 'Activate your account.'
                            to_email = user.email
                            send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                      to_email], fail_silently=False)
                            print("Mail send")
                        except Exception as e:
                            print(e)

                    profile_school.ref_user = user
                    profile_school.ref_organization = profile.ref_organization
                    group = Group.objects.get(name='school')
                    profile_school.save()
                    group.user_set.add(user)
                    print("School user create done")

                    return redirect('web:organization_school_user_list', pk=profile.ref_organization.id)

            else:
                form.add_error('', 'Form is not valid!')
        else:
            pass
        return render(request, 'auth/dashboard/create_school_user_by_organization.html', {'orga': profile, 'school': school, 'form': form})
    else:
        template_name = '404.html'
        title = 404
        kwvars = {'data': title, }
        return render(request, template_name, kwvars)


@login_required
@permission_required(['db.add_teacheruserprofile'], raise_exception=True)
def create_teacher_user_by_school(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            school = School.objects.get(id=pk)
            if logged_in_user == school.id:
                data = request.POST.dict()
                form = SchoolTeacherSignUpForm(
                    data or None, request.FILES or None)
                if request.method == 'POST':

                    if form.is_valid():
                        profile_teacher = form.save(commit=False)
                        first_name = data.get('first_name')
                        last_name = data.get('last_name')
                        email = data.get('email')
                        gender = data.get('gender')
                        date_of_birth = data.get('date_of_birth')
                        lang_one = data.get('lang_one')
                        lang_two = data.get('lang_two')
                        lang_three = data.get('lang_three')
                        avtar = data.get('avtar')
                        if User.objects.filter(email=email).exists():
                            form.add_error('', 'User already exists')
                            print("User already exists")
                        else:
                            user = User.objects.create_user(
                                username=email, email=email, first_name=first_name, last_name=last_name)
                            password = get_random_string(128)
                            user.is_active = False
                            user.set_password(password)
                            user.save()
                            ctoken = get_random_string(192)
                            pwd_reset_data = {"user": user.id, "token": ctoken}
                            pwd_reset_serializer = AuthForgetPasswordSerializer(
                                data=pwd_reset_data)
                            if pwd_reset_serializer.is_valid():
                                pwd_reset_serializer.save()
                                try:
                                    message = render_to_string('auth/acc_active_email.html', {
                                        "email": user.email,
                                        'user': user,
                                        'domain': request.headers['Host'],
                                        'site_name': 'Interface',
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': pwd_reset_serializer.data["token"],
                                        'protocol': 'http',
                                    })
                                    subject = 'Activate your account.'
                                    to_email = user.email
                                    send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                              to_email], fail_silently=False)
                                    print("Mail send")
                                except Exception as e:
                                    print(e)

                            profile_teacher.ref_user = user
                            profile_teacher.ref_school = school
                            group = Group.objects.get(name='teacher')
                            profile_teacher.save()
                            group.user_set.add(user)
                            return redirect('web:deatil_school', pk=school.pk)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass
                return render(request, 'auth/school/create_teacher_user_by_school.html', {'form': form, 'school': school, 'cdate': current_day, 'pdate': previous_day})
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:

        try:
            school = School.objects.get(id=pk)
            if school.id:
                data = request.POST.dict()
                form = SchoolTeacherSignUpForm(
                    data or None, request.FILES or None)
                if request.method == 'POST':

                    if form.is_valid():
                        profile_teacher = form.save(commit=False)
                        first_name = data.get('first_name')
                        last_name = data.get('last_name')
                        email = data.get('email')
                        gender = data.get('gender')
                        date_of_birth = data.get('date_of_birth')
                        lang_one = data.get('lang_one')
                        lang_two = data.get('lang_two')
                        lang_three = data.get('lang_three')
                        avtar = data.get('avtar')
                        if User.objects.filter(email=email).exists():
                            form.add_error('', 'User already exists')
                            print("User already exists")
                        else:
                            user = User.objects.create_user(
                                username=email, email=email, first_name=first_name, last_name=last_name)
                            password = get_random_string(128)
                            user.is_active = False
                            user.set_password(password)
                            user.save()
                            ctoken = get_random_string(192)
                            pwd_reset_data = {"user": user.id, "token": ctoken}
                            pwd_reset_serializer = AuthForgetPasswordSerializer(
                                data=pwd_reset_data)
                            if pwd_reset_serializer.is_valid():
                                pwd_reset_serializer.save()
                                try:
                                    message = render_to_string('auth/acc_active_email.html', {
                                        "email": user.email,
                                        'user': user,
                                        'domain': request.headers['Host'],
                                        'site_name': 'Interface',
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': pwd_reset_serializer.data["token"],
                                        'protocol': 'http',
                                    })
                                    subject = 'Activate your account.'
                                    to_email = user.email
                                    send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                              to_email], fail_silently=False)
                                    print("Mail send")
                                except Exception as e:
                                    print(e)

                            profile_teacher.ref_user = user
                            profile_teacher.ref_school = school
                            group = Group.objects.get(name='teacher')
                            profile_teacher.save()
                            group.user_set.add(user)
                            return redirect('web:deatil_school', pk=school.pk)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass
                return render(request, 'auth/school/create_teacher_user_by_school.html', {'form': form, 'school': school, 'cdate': current_day, 'pdate': previous_day})
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True

    else:
        raise_permision_denied = True
    
    if raise_permision_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.add_schoolstudentuserprofile'], raise_exception=True)
def create_school_student_user_by_school_by_app_no(request):
    query = request.GET.get('apno')
    user = request.user
    # print(query)
    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            if Application.objects.filter(ap_code=query).exists():
                application = Application.objects.get(ap_code=query)

                # Get Application Services
                service_json_data = json.loads(
                    application.ap_service_json_data.replace("'", '"'))[0]

                applicaton_services = []
                for service_type in ['perweek', 'onetime']:
                    for service in service_json_data[service_type]:
                        s_name = service['p_service_name']
                        if service['p_service_type'] == 'Per Week':
                            s_type = 1
                        if service['p_service_type'] == 'One Time':
                            s_type = 2

                        s_services = SchoolService.objects.filter(
                            ref_school=application.ref_school, service_type=s_type, service_name=s_name)

                        if s_services:
                            applicaton_services.append(s_services.first().pk)
                # End Of Get Application Services

                if logged_in_user == application.ref_school.id:
                    data = request.POST.dict()
                    form = SchoolStudentSignUpForm(
                        data or None, request.FILES or None)
                    if request.method == 'POST':
                        if form.is_valid():
                            school_student_profile = form.save(commit=False)
                            first_name = data.get('first_name')
                            last_name = data.get('last_name')
                            gender = data.get('gender')
                            date_of_birth = data.get('date_of_birth')
                            home_address = data.get('home_address')
                            post_code = data.get('post_code')
                            nationality = data.get('nationality')
                            email = data.get('email')
                            phone = data.get('phone')
                            religion = data.get('religion')
                            passport_number = data.get('passport_number')
                            passport_expiry_date = data.get(
                                'passport_expiry_date')
                            avtar = data.get('avtar')
                            todays_date = date.today()
                            print(todays_date.year)
                            y = str(todays_date.year)
                            m = str(todays_date.month)
                            d = str(todays_date.day)
                            latest_id = User.objects.latest('id').id
                            current_save = latest_id+1
                            print(current_save)
                            date_format = y+m+d+str(latest_id)

                            print(date_format)
                            if User.objects.filter(username=email).exists():
                                form.add_error(
                                    '', 'Email already exists. Add new email.')
                                print("User already exists")
                            else:

                                with transaction.atomic():
                                    user = User.objects.create_user(
                                        username=date_format, email=email, first_name=first_name, last_name=last_name)
                                    password = get_random_string(128)
                                    user.is_active = False
                                    user.set_password(password)
                                    user.save()
                                    ctoken = get_random_string(192)
                                    pwd_reset_data = {
                                        "user": user.id, "token": ctoken}
                                    pwd_reset_serializer = AuthForgetPasswordSerializer(
                                        data=pwd_reset_data)
                                    if pwd_reset_serializer.is_valid():
                                        pwd_reset_serializer.save()
                                        try:
                                            message = render_to_string('auth/acc_active_email_school_student.html', {
                                                "email": user.email,
                                                'user': user,
                                                'user_name': user.username,
                                                'domain': request.headers['Host'],
                                                'site_name': 'Interface',
                                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                                'token': pwd_reset_serializer.data["token"],
                                                'protocol': 'http',
                                            })
                                            subject = 'Activate your account.'
                                            to_email = user.email
                                            send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                                to_email], fail_silently=False)
                                            print("Mail send")
                                        except Exception as e:
                                            print(e)

                                    school = School.objects.get(
                                        id=application.ref_school.id)
                                    school_student_profile.ref_user = user
                                    school_student_profile.ref_school = school
                                    group = Group.objects.get(
                                        name='school_student')
                                    school_student_profile.save()

                                    # Assign Student Course Level While Creating School Student Profile
                                    school_course_level = SchoolCourseLevel.objects.filter(
                                        ref_school=application.ref_school, name=application.ap_level)
                                    school_student_profile.ref_course_level = school_course_level.first()
                                    school_student_profile.save()
                                    # End Here

                                    # Add Student Course Details
                                    school_class = get_object_or_404(
                                        SchoolClass, pk=application.ap_course_class)
                                    school_student_user_profile = get_object_or_404(
                                        SchoolStudentUserProfile, ref_user=user)

                                    StudentProfileHasCourse.objects.create(
                                        ref_student=school_student_user_profile,
                                        ref_course=school_class,
                                        start_date=application.ap_start_date,
                                        end_date=application.ap_end_date,
                                        study_period=application.ap_study_period,
                                        installments=application.installments,
                                    )

                                    try:
                                        room_title_pk = re.search(
                                            "(?:'accommodation': \[{'id': )(\d*)", application.ap_json_data)[1]
                                        school_accommodation_service = get_object_or_404(
                                            SchoolAccommodationService, pk=room_title_pk)

                                        # Add Student Accommodation Details
                                        StudentProfileHasAccommodation.objects.create(
                                            ref_student=school_student_user_profile,
                                            ref_accommodation_room=school_accommodation_service,
                                            start_date=application.ap_start_date,
                                            end_date=application.ap_end_date,
                                            payment=True,
                                        )
                                    except:
                                        pass

                                    try:
                                        for app_service in applicaton_services:

                                            school_service = get_object_or_404(
                                                SchoolService, pk=app_service)

                                            # Add Student Accommodation Details
                                            StudentProfileHasService.objects.create(
                                                ref_student=school_student_user_profile,
                                                ref_service=school_service,
                                                start_date=application.ap_start_date,
                                                end_date=application.ap_end_date,
                                                payment=True,
                                            )
                                    except:
                                        pass

                                    group.user_set.add(user)

                                return redirect('web:deatil_school', pk=school.pk)
                        else:
                            print("Form is not valid")
                            error = "Form is not valid"
                            form.add_error(None, error)
                            print(form.errors)
                    else:
                        pass
                    return render(request, 'auth/school/create_school_student_user_by_school_by_app_no.html', {'data': application, 'form': form})
                else:
                    permission = "permission"
                    return render(request, 'auth/school/create_school_student_user_by_school_by_app_no.html', {'permission': permission})
            else:
                permission = "permission"
                return render(request, 'auth/school/create_school_student_user_by_school_by_app_no.html', {'permission': permission})

        except School.DoesNotExist:
            permission = "permission"
            return render(request, 'auth/school/create_school_student_user_by_school_by_app_no.html', {'permission': permission})
    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            if Application.objects.filter(ap_code=query).exists():
                application = Application.objects.get(ap_code=query)
                if application.ref_school.id:
                    data = request.POST.dict()
                    form = SchoolStudentSignUpForm(
                        data or None, request.FILES or None)
                    if request.method == 'POST':
                        if form.is_valid():
                            school_student_profile = form.save(commit=False)
                            first_name = data.get('first_name')
                            last_name = data.get('last_name')
                            gender = data.get('gender')
                            date_of_birth = data.get('date_of_birth')
                            home_address = data.get('home_address')
                            post_code = data.get('post_code')
                            nationality = data.get('nationality')
                            email = data.get('email')
                            phone = data.get('phone')
                            religion = data.get('religion')
                            passport_number = data.get('passport_number')
                            passport_expiry_date = data.get(
                                'passport_expiry_date')
                            avtar = data.get('avtar')
                            todays_date = date.today()
                            print(todays_date.year)
                            y = str(todays_date.year)
                            m = str(todays_date.month)
                            d = str(todays_date.day)
                            latest_id = User.objects.latest('id').id
                            current_save = latest_id+1
                            print(current_save)
                            date_format = y+m+d+str(latest_id)

                            print(date_format)
                            if User.objects.filter(username=email).exists():
                                form.add_error(
                                    '', 'Email already exists. Add new email.')
                                print("User already exists")
                            else:
                                with transaction.atomic():
                                    user = User.objects.create_user(
                                        username=date_format, email=email, first_name=first_name, last_name=last_name)
                                    password = get_random_string(128)
                                    user.is_active = False
                                    user.set_password(password)
                                    user.save()
                                    ctoken = get_random_string(192)
                                    pwd_reset_data = {
                                        "user": user.id, "token": ctoken}
                                    pwd_reset_serializer = AuthForgetPasswordSerializer(
                                        data=pwd_reset_data)
                                    if pwd_reset_serializer.is_valid():
                                        pwd_reset_serializer.save()
                                        try:
                                            message = render_to_string('auth/acc_active_email_school_student.html', {
                                                "email": user.email,
                                                'user': user,
                                                'user_name': user.username,
                                                'domain': request.headers['Host'],
                                                'site_name': 'Interface',
                                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                                'token': pwd_reset_serializer.data["token"],
                                                'protocol': 'http',
                                            })
                                            subject = 'Activate your account.'
                                            to_email = user.email
                                            send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                                to_email], fail_silently=False)
                                            print("Mail send")
                                        except Exception as e:
                                            print(e)

                                    school = School.objects.get(
                                        id=application.ref_school.id)
                                    school_student_profile.ref_user = user
                                    school_student_profile.ref_school = school
                                    group = Group.objects.get(
                                        name='school_student')
                                    school_student_profile.save()

                                    # Assign Student Course Level While Creating School Student Profile
                                    school_course_level = SchoolCourseLevel.objects.filter(
                                        ref_school=application.ref_school, name=application.ap_level)
                                    school_student_profile.ref_course_level = school_course_level.first()
                                    school_student_profile.save()
                                    # End Here

                                    # Add Student Course Details
                                    school_class = get_object_or_404(
                                        SchoolClass, pk=application.ap_course_class)
                                    school_student_user_profile = get_object_or_404(
                                        SchoolStudentUserProfile, ref_user=user)

                                    StudentProfileHasCourse.objects.create(
                                        ref_student=school_student_user_profile,
                                        ref_course=school_class,
                                        start_date=application.ap_start_date,
                                        end_date=application.ap_end_date,
                                        study_period=application.ap_study_period,
                                    )

                                    try:
                                        room_title_pk = re.search(
                                            "(?:'accommodation': \[{'id': )(\d*)", application.ap_json_data)[1]
                                        school_accommodation_service = get_object_or_404(
                                            SchoolAccommodationService, pk=room_title_pk)

                                        # Add Student Accommodation Details
                                        StudentProfileHasAccommodation.objects.create(
                                            ref_student=school_student_user_profile,
                                            ref_accommodation_room=school_accommodation_service,
                                            start_date=application.ap_start_date,
                                            end_date=application.ap_end_date,
                                            payment=True,
                                        )
                                    except:
                                        pass

                                    try:
                                        for app_service in applicaton_services:

                                            school_service = get_object_or_404(
                                                SchoolService, pk=app_service)

                                            # Add Student Service Details
                                            StudentProfileHasService.objects.create(
                                                ref_student=school_student_user_profile,
                                                ref_service=school_service,
                                                start_date=application.ap_start_date,
                                                end_date=application.ap_end_date,
                                                payment=True,
                                            )
                                    except:
                                        pass

                                    group.user_set.add(user)
                                return redirect('web:deatil_school', pk=school.pk)
                        else:
                            print("Form is not valid")
                            error = "Form is not valid"
                            form.add_error(None, error)
                            print(form.errors)
                    else:
                        pass
                    return render(request, 'auth/school/create_school_student_user_by_school_by_app_no.html', {'data': application, 'form': form})
                else:
                    permission = "permission"
                    return render(request, 'auth/school/create_school_student_user_by_school_by_app_no.html', {'permission': permission})
            else:
                permission = "permission"
                return render(request, 'auth/school/create_school_student_user_by_school_by_app_no.html', {'permission': permission})

        except School.DoesNotExist:
            permission = "permission"
            return render(request, 'auth/school/create_school_student_user_by_school_by_app_no.html', {'permission': permission})


@login_required
@permission_required(['db.add_schoolstudentuserprofile'], raise_exception=True)
def create_school_student_user_by_school(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            school = School.objects.get(id=pk)
            if logged_in_user == school.id:
                data = request.POST.dict()
                form = SchoolStudentSignUpForm(
                    data or None, request.FILES or None)
                if request.method == 'POST':

                    if form.is_valid():
                        school_student_profile = form.save(commit=False)
                        first_name = data.get('first_name')
                        last_name = data.get('last_name')
                        gender = data.get('gender')
                        date_of_birth = data.get('date_of_birth')
                        home_address = data.get('home_address')
                        post_code = data.get('post_code')
                        nationality = data.get('nationality')
                        email = data.get('email')
                        phone = data.get('phone')
                        religion = data.get('religion')
                        passport_number = data.get('passport_number')
                        passport_expiry_date = data.get('passport_expiry_date')
                        avtar = data.get('avtar')
                        todays_date = date.today()
                        y = str(todays_date.year)
                        m = str(todays_date.month)
                        d = str(todays_date.day)
                        latest_id = User.objects.latest('id').id
                        current_save = latest_id+1
                        print(current_save)
                        date_format = y+m+d+str(latest_id)

                        if User.objects.filter(username=email).exists():
                            form.add_error(
                                '', 'Email already exists. Add new email.')
                            print("Email already exists")
                        else:
                            ''' Checking valid mobile number using phonenumbers '''
                            phone_number = phone
                            print('Mobile Number: ', phone_number)
                            try:
                                validate_number = phonenumbers.parse(
                                    phone_number, None)
                                print(validate_number)
                                if phonenumbers.is_valid_number(validate_number):
                                    print('Valid Mobile Number: ', phone_number)

                                    user = User.objects.create_user(
                                        username=date_format, email=email, first_name=first_name, last_name=last_name)
                                    password = get_random_string(128)
                                    user.is_active = False
                                    user.set_password(password)
                                    user.save()
                                    ctoken = get_random_string(192)
                                    pwd_reset_data = {
                                        "user": user.id, "token": ctoken}
                                    pwd_reset_serializer = AuthForgetPasswordSerializer(
                                        data=pwd_reset_data)
                                    if pwd_reset_serializer.is_valid():
                                        pwd_reset_serializer.save()
                                        try:
                                            message = render_to_string('auth/acc_active_email_school_student.html', {
                                                "email": user.email,
                                                'user': user,
                                                'user_name': user.username,
                                                'domain': request.headers['Host'],
                                                'site_name': 'Interface',
                                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                                'token': pwd_reset_serializer.data["token"],
                                                'protocol': 'http',
                                            })
                                            subject = 'Activate your account.'
                                            to_email = user.email
                                            send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                                      to_email], fail_silently=False)
                                            print("Mail send")
                                        except Exception as e:
                                            print(e)

                                    school_student_profile.ref_user = user
                                    school_student_profile.ref_school = school
                                    group = Group.objects.get(
                                        name='school_student')
                                    school_student_profile.save()
                                    group.user_set.add(user)
                                    return redirect('web:deatil_school', pk=school.pk)
                                else:
                                    print('Invalid Mobile Number: ',
                                          phone_number)
                                    error = f"Please enter a valid mobile number: {phone_number}"
                                    form.add_error(None, error)
                            except phonenumbers.phonenumberutil.NumberParseException:
                                print(
                                    "phonenumbers.phonenumberutil.NumberParseException")
                                error = f"Please enter a valid mobile number: {phone_number}"
                                form.add_error(None, error)
                                print(form.errors)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass
                return render(request, 'auth/school/create_school_student_user_by_school.html', {'school': school, 'form': form, 'cdate': current_day, 'pdate': previous_day})
            else:
                raise_permission_denied = True
        except School.DoesNotExist:

            raise_permission_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            school = School.objects.get(id=pk)
            if school.id:
                data = request.POST.dict()
                form = SchoolStudentSignUpForm(
                    data or None, request.FILES or None)
                if request.method == 'POST':

                    if form.is_valid():
                        school_student_profile = form.save(commit=False)
                        first_name = data.get('first_name')
                        last_name = data.get('last_name')
                        gender = data.get('gender')
                        date_of_birth = data.get('date_of_birth')
                        home_address = data.get('home_address')
                        post_code = data.get('post_code')
                        nationality = data.get('nationality')
                        email = data.get('email')
                        phone = data.get('phone')
                        religion = data.get('religion')
                        passport_number = data.get('passport_number')
                        passport_expiry_date = data.get('passport_expiry_date')
                        avtar = data.get('avtar')
                        todays_date = date.today()
                        y = str(todays_date.year)
                        m = str(todays_date.month)
                        d = str(todays_date.day)
                        latest_id = User.objects.latest('id').id
                        current_save = latest_id+1
                        print(current_save)
                        date_format = y+m+d+str(latest_id)

                        if User.objects.filter(username=email).exists():
                            form.add_error(
                                '', 'Email already exists. Add new email.')
                            print("Emial already exists")
                        else:
                            ''' Checking valid mobile number using phonenumbers '''
                            phone_number = phone
                            print('Mobile Number: ', phone_number)
                            try:
                                validate_number = phonenumbers.parse(
                                    phone_number, None)
                                print(validate_number)
                                if phonenumbers.is_valid_number(validate_number):
                                    print('Valid Mobile Number: ', phone_number)

                                    user = User.objects.create_user(
                                        username=date_format, email=email, first_name=first_name, last_name=last_name)
                                    password = get_random_string(128)
                                    user.is_active = False
                                    user.set_password(password)
                                    user.save()
                                    ctoken = get_random_string(192)
                                    pwd_reset_data = {
                                        "user": user.id, "token": ctoken}
                                    pwd_reset_serializer = AuthForgetPasswordSerializer(
                                        data=pwd_reset_data)
                                    if pwd_reset_serializer.is_valid():
                                        pwd_reset_serializer.save()
                                        try:
                                            message = render_to_string('auth/acc_active_email_school_student.html', {
                                                "email": user.email,
                                                'user': user,
                                                'user_name': user.username,
                                                'domain': request.headers['Host'],
                                                'site_name': 'Interface',
                                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                                'token': pwd_reset_serializer.data["token"],
                                                'protocol': 'http',
                                            })
                                            subject = 'Activate your account.'
                                            to_email = user.email
                                            send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                                      to_email], fail_silently=False)
                                            print("Mail send")
                                        except Exception as e:
                                            print(e)

                                    school_student_profile.ref_user = user
                                    school_student_profile.ref_school = school
                                    group = Group.objects.get(
                                        name='school_student')
                                    school_student_profile.save()
                                    group.user_set.add(user)
                                    return redirect('web:deatil_school', pk=school.pk)
                                else:
                                    print('Invalid Mobile Number: ',
                                          phone_number)
                                    error = f"Please enter a valid mobile number: {phone_number}"
                                    form.add_error(None, error)
                            except phonenumbers.phonenumberutil.NumberParseException:
                                print(
                                    "phonenumbers.phonenumberutil.NumberParseException")
                                error = f"Please enter a valid mobile number: {phone_number}"
                                form.add_error(None, error)
                                print(form.errors)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass
                return render(request, 'auth/school/create_school_student_user_by_school.html', {'school': school, 'form': form, 'cdate': current_day, 'pdate': previous_day})
            else:
                raise_permission_denied = True
        except School.DoesNotExist:

            raise_permission_denied = True

    else:
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


def sign_up(request):
    # redirect_url = '/admin-index/'
    data = request.POST.dict()
    form = SignUpForm(data or None, request.FILES or None)

    if request.method == 'POST':

        if form.is_valid():
            profile = form.save(commit=False)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            password = data.get('password')
            email = data.get('email')

            if User.objects.filter(email=email).exists():
                form.add_error('', 'User already exists')
                print("User already exists")

            else:

                user = User.objects.create_user(
                    username=email, email=email, first_name=first_name, last_name=last_name, password=password)
                password = get_random_string(128)
                user.is_active = True
                user.set_password(password)
                user.save()
                ctoken = get_random_string(192)
                pwd_reset_data = {"user": user.id, "token": ctoken}
                pwd_reset_serializer = AuthForgetPasswordSerializer(
                    data=pwd_reset_data)

                if pwd_reset_serializer.is_valid():
                    pwd_reset_serializer.save()
                    print("Token================================================")
                    print(pwd_reset_serializer.data["token"])

                    try:
                        message = render_to_string('auth/acc_active_email.html', {
                            "email": user.email,
                            'user': user,
                            'domain': request.headers['Host'],
                            'site_name': 'Interface',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': pwd_reset_serializer.data["token"],
                            'protocol': 'http',
                        })
                        # print(message)
                        subject = 'Activate your account.'
                        to_email = form.cleaned_data.get('email')
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                  to_email], fail_silently=False)
                        print("Mail send")
                    except Exception as e:
                        print(e)

                profile.ref_user = user
                group = Group.objects.get(name='staff')
                profile.save()
                group.user_set.add(user)
                pass

                # return redirect('')

                # return redirect(redirect_url)
        else:
            form.add_error('', 'Form is not valid')

    return render(request, 'auth/sign_up.html', {'form': form})


def sign_up_student(request):
    # redirect_url = '/admin-index/'
    data = request.POST.dict()
    form = StudentSignUpForm(data or None, request.FILES or None)

    if request.method == 'POST':

        if form.is_valid():
            profile = form.save(commit=False)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')

            if User.objects.filter(email=email).exists():
                form.add_error('', 'Email already exists')

            else:

                user = User.objects.create_user(
                    username=email, email=email, first_name=first_name, last_name=last_name)
                password = get_random_string(128)
                user.is_active = True
                user.set_password(password)
                user.save()
                ctoken = get_random_string(192)
                pwd_reset_data = {"user": user.id, "token": ctoken}
                pwd_reset_serializer = AuthForgetPasswordSerializer(
                    data=pwd_reset_data)

                if pwd_reset_serializer.is_valid():
                    pwd_reset_serializer.save()

                    try:
                        message = render_to_string('auth/acc_active_email.html', {
                            "email": user.email,
                            'user': user,
                            'domain': request.headers['Host'],
                            'site_name': 'Interface',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': pwd_reset_serializer.data["token"],
                            'protocol': 'http',
                        })

                        subject = 'Activate your account.'
                        to_email = user.email
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                  to_email], fail_silently=False)
                    except Exception as e:
                        print(e)

                profile.ref_user = user
                group = Group.objects.get(name='student')
                profile.save()
                group.user_set.add(user)
                return render(request, 'auth/sign_up_succes.html')
        else:
            form.add_error('', 'Form is not valid')

    return render(request, 'auth/sign_up_student.html', {'form': form})


def sign_up_aggent(request):
    # redirect_url = '/admin-index/'
    data = request.POST.dict()
    form = AgentSignUpForm(data or None, request.FILES or None)

    if request.method == 'POST':

        if form.is_valid():
            profile = form.save(commit=False)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')

            if User.objects.filter(email=email).exists():
                form.add_error('', 'Email already exists')

            else:

                user = User.objects.create_user(
                    username=email, email=email, first_name=first_name, last_name=last_name)
                password = get_random_string(128)
                user.is_active = True
                user.set_password(password)
                user.save()
                ctoken = get_random_string(192)
                pwd_reset_data = {"user": user.id, "token": ctoken}
                pwd_reset_serializer = AuthForgetPasswordSerializer(
                    data=pwd_reset_data)

                if pwd_reset_serializer.is_valid():
                    pwd_reset_serializer.save()

                    try:
                        message = render_to_string('auth/acc_active_email.html', {
                            "email": user.email,
                            'user': user,
                            'domain': request.headers['Host'],
                            'site_name': 'Interface',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': pwd_reset_serializer.data["token"],
                            'protocol': 'http',
                        })
                        subject = 'Activate your account.'
                        to_email = user.email
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                  to_email], fail_silently=False)
                        print("Mail send")
                    except Exception as e:
                        print(e)

                profile.ref_user = user
                group = Group.objects.get(name='aggent')
                profile.save()
                group.user_set.add(user)
                return render(request, 'auth/sign_up_succes.html')
        else:
            form.add_error('', 'Form is not valid')

    return render(request, 'auth/sign_up_aggent.html', {'form': form})


class DeleteUser(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('auth.delete_user')
    model = User
    template_name = 'auth/dashboard/delete_user.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:create_user_page')

    def get_context_data(self, **kwargs):
        user_id = self.kwargs.get('pk', None)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete'
        context['content'] = 'Are you sure you want to delete ?'
        return context


class DeleteStudent(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_studentuserprofile')
    model = StudentUserProfile
    template_name = 'auth/dashboard/delete_student.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:create_user_page')

    def get_context_data(self, **kwargs):
        student_id = self.kwargs.get('pk', None)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete'
        context['content'] = 'Are you sure you want to delete ?'
        return context


class DeleteAgent(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_aggentuserprofile')
    model = AggentUserProfile
    template_name = 'auth/dashboard/delete_agent.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:create_user_page')

    def get_context_data(self, **kwargs):
        student_id = self.kwargs.get('pk', None)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete'
        context['content'] = 'Are you sure you want to delete ?'
        return context


class DeleteStaffAndAdmin(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_userprofile')
    model = UserProfile
    template_name = 'auth/dashboard/delete_agent_and_admin.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:create_user_page')

    def get_context_data(self, **kwargs):
        profile_id = self.kwargs.get('pk', None)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete'
        context['content'] = 'Are you sure you want to delete ?'
        return context


class AuthForgetPasswordViewset(CreateView):

    template_name = 'auth/password_reset.html'
    form_class = SetPasswordForm

    def get(self, request, *args, **kwargs):
        _token = kwargs['token']
        if _token is not None:
            today = datetime.datetime.now()
            start = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + datetime.timedelta(1)

            _start_date = start.strftime("%Y-%m-%d %H:%M:%S")
            _end_date = end.strftime("%Y-%m-%d %H:%M:%S")

            # created_at__range=(_start_date, _end_date)
            _model = AuthForgetPasswordToken.objects.filter(
                token=_token)
            ctoken = ""
            for token_in in _model:

                ctoken = token_in.token
            ctx = {
                "ctoken": ctoken
            }
            if _model.exists():
                return render(request, 'auth/password_reset.html', ctx)
            else:
                return render(request, 'auth/invalid_token_link.html')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()

        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')
        token = data.get('token')
        print(token)

        if token is not None and new_password1 is not None and new_password2:
            if new_password1 != new_password2:
                print("messege password not match")
                pass
            else:
                token_model = AuthForgetPasswordToken.objects.filter(
                    token=token)
                if token_model.exists():
                    user = User.objects.filter(id=token_model.get().user_id)
                    if user.exists():
                        user_model = user.get()
                        user_model.set_password(new_password1)
                        user_model.is_active = True
                        user_model.save()
                        token_model.get().delete()
                        print("password change succes")
                        return redirect('web:login_page')
                    else:
                        print("User cannot exist")
                        pass
                else:
                    print("this url can not exist")
                    pass
        else:
            print("Password requird")
            pass


@login_required
def user_permission_change(request, pk):
    user = request.user
    if user.is_superuser:
        user_model = User.objects.get(pk=pk)
        print(user_model.is_active)

        status = request.GET.get('status')
        if status == 'deactivate':
            if user_model.is_active == True:
                user_model.is_active = False
                user_model.save()
                return redirect('web:create_user_page')
        elif status == 'active':
            if user_model.is_active == False:
                user_model.is_active = True
                user_model.save()
                return redirect('web:create_user_page')

            else:
                print("Do some action")

    elif user.groups.filter(name='admin').exists():
        print("admin")

    else:
        permission = "permission"
        return render(request, '', {'permission': permission})
