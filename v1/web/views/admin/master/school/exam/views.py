from ast import mod
from unicodedata import category
from django.shortcuts import get_object_or_404, render, redirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from v1.db.models import *

from .forms import *

from v1.base.configs import cRequest


@login_required
@permission_required(['db.add_schoolexam'], raise_exception=True)
def SchoolExamCreate(request, pk):
    user = request.user
    raise_permision_denied = False
    
    m_course = get_object_or_404(SchoolCourse, pk=pk)
    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            school = m_course.ref_school
            if logged_in_user == school.id:

                context = {}

                # school = School.objects.filter(pk=pk)
                # school = school.first()

                form = SchoolExamForm(
                    request.POST or None, course_id=m_course.pk)

                data = request.POST.dict()
                if request.method == 'POST':
                    if form.is_valid():
                        if form.save():
                            return redirect('web:details_school_course', pk=pk)
                        else:
                            print(form.errors)
                    else:
                        print(form.errors)

                context['title'] = 'Add School Exam'
                context['course'] = m_course
                context['school'] = school
                context['form'] = form

                return render(request, 'admin/school/exam/create.html', context)
            else:
                raise_permision_denied = True

        except School.DoesNotExist:
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            school = m_course.ref_school
            if school.id:

                context = {}

                # school = School.objects.filter(pk=pk)
                # school = school.first()

                form = SchoolExamForm(
                    request.POST or None, course_id=m_course.pk)

                data = request.POST.dict()
                if request.method == 'POST':
                    if form.is_valid():
                        if form.save():
                            return redirect('web:details_school_course', pk=pk)
                        else:
                            print(form.errors)
                    else:
                        print(form.errors)

                context['title'] = 'Add School Exam'
                context['school'] = school
                context['course'] = m_course
                context['form'] = form

                return render(request, 'admin/school/exam/create.html', context)
            else:
                raise_permision_denied = True

        except School.DoesNotExist:
            raise_permision_denied = True

    else:
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()