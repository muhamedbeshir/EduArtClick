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
from v1.db.models import *
from v1.web.utils import CHECK_USER_PERMISSION

from .forms import *

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError

current_day = date.today()
previous_day = date.today() - timedelta(days=1)


@login_required
@permission_required(['db.add_schoolcourse'], raise_exception=True)
def create_school_course(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            school = School.objects.get(id=pk)
            if logged_in_user == school.id:
                form = SchoolCourseForm(
                    request.POST or None, logged_in_user=logged_in_user)
                context = {}

                school = School.objects.filter(pk=pk)
                school = school.first()

                data = request.POST.dict()
                if request.method == 'POST':
                    if form.is_valid():
                        try:
                            course = form.save(commit=False)

                            course.ref_school = school
                            course.save()

                            print("Successfully =====================")
                            return redirect('web:deatil_school', pk=logged_in_user)
                        except IntegrityError:
                            error = "School Course should be unique."
                            form.add_error(None, error)
                    else:
                        print("form=====================Error=============")
                        print(form.errors)

                context['school'] = school
                context['form'] = form

                print(context)
                return render(request, 'admin/master/course/create_school_course.html', context)
            else:
                raise_permision_denied = True

        except School.DoesNotExist:
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            school = School.objects.get(id=pk)
            if school.id:

                context = {}

                school = School.objects.filter(pk=pk)
                school = school.first()
                #
                form = SchoolCourseForm(
                    request.POST or None, logged_in_user=school.id)

                data = request.POST.dict()
                if request.method == 'POST':
                    if form.is_valid():
                        try:
                            course = form.save(commit=False)

                            course.ref_school = school
                            course.save()

                            print("Successfully =====================")
                            return redirect('web:deatil_school', pk=school.id)
                        except IntegrityError:
                            error = "School Course should be unique."
                            form.add_error(None, error)
                    else:
                        print("form=====================Error=============")
                        print(form.errors)

                context['school'] = school
                context['form'] = form

                print(context)
                return render(request, 'admin/master/course/create_school_course.html', context)
            else:
                raise_permision_denied = True

        except School.DoesNotExist:
            raise_permision_denied = True

    else:
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()

@login_required
@permission_required(['db.change_schoolcourse'], raise_exception=True)
def update_school_course(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            queryset = SchoolCourse.objects.get(id=pk)
            if logged_in_user == queryset.ref_school.id:
                data = request.POST.dict()
                print('<=>'*10, data)
                form = SchoolCourseForm(
                    request.POST or None, instance=queryset, logged_in_user=logged_in_user)
                if request.method == 'POST':
                    print('1'*10, queryset)
                    print(request.POST)
                    # form = SchoolCourseEditForm(request.POST, instance=queryset)
                    # print(form)
                    if form.is_valid():
                        print(form.cleaned_data)
                        try:
                            form.save()
                            print("Successfully edit data")
                            return redirect('web:deatil_school', pk=queryset.ref_school.id)
                        except IntegrityError:
                            error = "School Course should be unique."
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = SchoolCourseForm(
                        request.POST or None, instance=queryset, logged_in_user=logged_in_user)

                template_name = 'admin/master/course/edit_school_course.html'
                kwvars = {
                    'course': queryset,
                    'form': form,
                }

                return render(request, template_name, kwvars)

            else:
                raise_permision_denied = True
        except SchoolCourse.DoesNotExist:
            raise_permision_denied = True
    else:
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()

class SchoolCourseUpdateView(LoginRequiredMixin, UpdateView):
    model = SchoolCourse
    form_class = SchoolCourseForm
    template_name = 'admin/master/course/create_school_course.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()
        self.PriceFormset = formset_factory(SchoolCoursePriceForm)

    def get_success_url(self):
        return reverse('web:deatil_school', args=(self.object.ref_school.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courseprice = list(SchoolCoursePrice.objects.filter(
            ref_school_course=self.object.id).values('min_weak', 'max_weak', 'price'))

        context['formset'] = self.PriceFormset(
            prefix='rel_ref_school_school_course', initial=courseprice)
        context['title'] = "Edit"
        return context

    def form_valid(self, form):
        user = self.request.user
        print(user)
        instance = form.save()
        formset = self.PriceFormset(
            self.request.POST, prefix='rel_ref_school_school_course')
        if formset.is_valid():
            print('formset')
            total_forms = int(formset.data.get(
                'rel_ref_school_school_course-TOTAL_FORMS'))
            if total_forms > 0:
                SchoolCoursePrice.objects.filter(
                    ref_school_course=self.object.id).delete()
                for i in range(total_forms):

                    price = formset.data.get(
                        'rel_ref_school_school_course-' + str(i) + '-price')
                    min_weak = formset.data.get(
                        'rel_ref_school_school_course-' + str(i) + '-min_weak')
                    max_weak = formset.data.get(
                        'rel_ref_school_school_course-' + str(i) + '-max_weak')
                    if price and min_weak:
                        courseprice = SchoolCoursePrice(
                            price=price, min_weak=min_weak, max_weak=max_weak, ref_school_course=instance)
                        courseprice.save()
        messages.success(self.request, 'Successfully Update.')
        return super(SchoolCourseUpdateView, self).form_valid(form)


class SchoolCourseDetails(PermissionRequiredMixin, DetailView):
    permission_required = ('db.view_schoolcourse',)
    template_name = 'admin/master/course/course_detail.html'
    model = SchoolCourse
    context_object_name = 'course'
    pk_url_kwarg = 'pk'


    def get_context_data(self, **kwargs):
        context = super(__class__, self).get_context_data(**kwargs)
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
                
        context['exams'] = SchoolExam.objects.filter(
            ref_course__ref_course=self.object)
        context['certificates'] = SchoolCertificateContent.objects.filter(
            ref_course__ref_course=self.object)
        context['class'] = SchoolClass.objects.filter(
            ref_course=self.object)
        # Compare Two Dates, If Valid Upto Date Expire then set to "False"
        discounts = SchoolCourseDiscount.objects.filter(
            ref_course=self.object)
        for discount in discounts:
            if discount.valid_upto < current_day:
                # print('[*] Invalid Coupon')
                discount.is_active = False
                discount.save()
        context['discounts'] = discounts
        context['levelupexams'] = SelectiveStudentExam.objects.filter(
            ref_course__ref_course=self.object)
        context['timetables'] = ClassTimeTable.objects.filter(
            ref_course=self.object)
        
        return context
         

@login_required
def create_school_course_price(request, pk):
    course = SchoolCourse.objects.filter(pk=pk)
    course = course.first()
    context = {}

    # print(course.ref_school.id)

    PriceFormset = modelformset_factory(
        SchoolCoursePrice, form=SchoolCoursePriceForm)
    formset = PriceFormset(request.POST or None, queryset=SchoolCourse.objects.none(
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


# class SchoolCourseDetails(LoginRequiredMixin, DetailView):
# 	model = SchoolCourse
# 	context_object_name = 'course'
# 	template_name = 'admin/course/details.html'

# 	def get_user(self):
# 		return self.request.user

# 	def get_context_data(self,**kwargs):
# 		user=self.get_user()

# 		if user.groups.filter(name='school').exists():
# 			course_id = self.kwargs.get('pk', None)
# 			course_query = SchoolCourse.objects.filter(id=course_id,ref_school=user.organizationuserprofile.ref_school)
# 			if course_query.exists():
# 				course = course_query.get()
# 				context = super(__class__,self).get_context_data(**kwargs)
# 				context["course"] = course
# 				context['price'] = SchoolCoursePrice.objects.filter(ref_school_course=course).order_by("id")
# 				context['student'] = StudentProfileHasCourse.objects.filter(ref_course=course).order_by("id")
# 				return context

# 		elif user.groups.filter(name='teacher').exists():
# 			course_id = self.kwargs.get('pk', None)
# 			course_query = SchoolCourse.objects.filter(id=course_id,ref_teacher_name=user)
# 			if course_query.exists():
# 				course = course_query.get()
# 				context = super(__class__,self).get_context_data(**kwargs)
# 				context["course"] = course
# 				context['price'] = SchoolCoursePrice.objects.filter(ref_school_course=course).order_by("id")
# 				context['student'] = StudentProfileHasCourse.objects.filter(ref_course=course).order_by("id")
# 				return context

# 		elif user.groups.filter(name='admin').exists() or user.is_superuser:
# 			course_id = self.kwargs.get('pk', None)
# 			course_query = SchoolCourse.objects.filter(id=course_id)
# 			if course_query.exists():
# 				course = course_query.get()
# 				context = super(__class__,self).get_context_data(**kwargs)
# 				context["course"] = course
# 				context['price'] = SchoolCoursePrice.objects.filter(ref_school_course=course).order_by("id")
# 				context['student'] = StudentProfileHasCourse.objects.filter(ref_course=course).order_by("id")
# 				return context

# 		#context = super(SchoolExam,self).get_context_data(**kwargs)
# 		context = {}
# 		context["permission"] = "permission"
# 		return context
