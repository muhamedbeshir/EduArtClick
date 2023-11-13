from datetime import date, timedelta
from typing import Any, Dict, List
from django.utils import timezone
import json
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Max, Min
from django.http import JsonResponse
from django.contrib.auth.models import User
from v1.db.models import *
from v1.db.school.school_sponsor import SchoolSponsor
from django.core.exceptions import PermissionDenied

from v1.web.utils import CHECK_USER_PERMISSION
from .forms import *

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError


current_day = date.today()


def checking_user_permission(request, object):
    user = request.user # Current User
    group = user.groups.first().name # Current User Group
    raise_exception = False

    # For Admin, Staff and Super Admin
    # 
    # For School
    if group == 'school':
        if not (user.organizationuserprofile.ref_school == object.ref_school):
            raise_exception = True
    # For Organization
    elif group == 'organization':
        if not (user.organizationuserprofile.ref_organization == object.ref_organization):
            raise_exception = True

    if raise_exception:
        raise PermissionDenied()




def school_create_view(request):
    context = {}
    SchoolServiceFormset = modelformset_factory(
        SchoolService, form=SchoolServiceForm)
    # SchoolCourseFormset = modelformset_factory(SchoolCourse, form=SchoolCourseForm)
    form = SchoolForm(request.POST or None, request.FILES or None)
    service_formset = SchoolServiceFormset(
        request.POST or None, queryset=SchoolService.objects.none(), prefix='rel_ref_school_service')
    # course_formset = SchoolCourseFormset(request.POST or None, queryset= SchoolCourse.objects.none(), prefix='rel_ref_school_school_course')
    if request.method == "POST":
        if form.is_valid() and service_formset.is_valid():
            try:
                with transaction.atomic():
                    school = form.save(commit=False)
                    school.save()

                    for rel_ref_school_service in service_formset:
                        data = rel_ref_school_service.save(commit=False)
                        data.save()
            except IntegrityError:
                print("Error Encountered")

            return redirect('web:school_list')

    context['service_formset'] = service_formset
    # context['course_formset'] = course_formset
    context['form'] = form
    context['title'] = "Add"
    return render(request, 'admin/master/add_school.html', context)


class SchoolCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('db.add_school')
    model = School
    form_class = SchoolForm

    def __init__(self):
        super().__init__()

    def get_template_names(self) -> List[str]:
        template_name = 'admin/master/add_school.html'
        template_name_organization = 'admin/master/add_school_organization.html'
        
        # Only for organization user
        if not self.request.user.is_superuser:
            if self.request.user.groups.all().first().name == 'organization':
                return template_name_organization
        return template_name

    def get_success_url(self):
        return reverse_lazy('web:deatil_school', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add School"
        # Only for organization user
        if not self.request.user.is_superuser:
            if self.request.user.groups.all().first().name == 'organization':
                context['organization'] = self.request.user.organizationuserprofile.ref_organization

        return context
 

    def form_valid(self, form):
        user = self.request.user
        instance = form.save(commit=False)

        # Only for organization user
        if not user.is_superuser:
            if user.groups.all().first().name == 'organization':
                # Check user organization and school organization, if both match then create new school
                # Otherwise raise an error
                if not user.organizationuserprofile.ref_organization == instance.ref_organization:
                    form.add_error('', "You can't add school in other organization")
                    return super(SchoolCreateView, self).form_invalid(form)
                
        instance.save()

        messages.success(self.request, 'Successfully Added.')
        return super(SchoolCreateView, self).form_valid(form)


class ListSchool(PermissionRequiredMixin, ListView):
    permission_required = ('db.view_school')
    model = School
    context_object_name = 'schools'
    template_name = 'admin/master/school_list.html'

    def get_user_role(self):
        role = None
        try:
            user = self.request.user
            if user.is_superuser:
                role = "admin"
            else:
                roles = user.groups.filter().all()
                for _role in roles:
                    role = _role.name
        except Exception as e:
            pass
        return role

    def get_queryset(self):
        role = self.get_user_role()
        # print(self.request.user.organizationuserprofile.ref_organization.id)
        if (role == "organization"):
            queryset = School.objects.filter(
                ref_organization=self.request.user.organizationuserprofile.ref_organization.id).order_by("-id")
        else:
            queryset = School.objects.all().order_by("-id")
        return queryset


class EditSchool(PermissionRequiredMixin, UpdateView):
    permission_required = ('db.change_school')
    model = School
    form_class = SchoolForm
    template_name = 'admin/master/edit_school.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:deatil_school', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit School"
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Successfully Update.')
        return super(EditSchool, self).form_valid(form)


class DeleteSchool(PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_school')
    model = School
    template_name = 'admin/master/delete_school.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('web:school_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete School'
        context['content'] = 'Are you sure you want to delete ?'
        return context


class DetailSchool(PermissionRequiredMixin, DetailView):
    permission_required = ('db.view_school')
    model = School
    context_object_name = 'schools'
    template_name = 'admin/master/school_detail.html'

    def get_user(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object)
        user = self.get_user()
        raise_permission_denied = False

        if user.groups.filter(name='school').exists():
            logged_in_user = user.organizationuserprofile.ref_school.id
            school_id = self.kwargs.get('pk', None)
            school = School.objects.get(id=school_id)
            if logged_in_user == school.id:
                context = super(DetailSchool, self).get_context_data(**kwargs)
                context['accommodation_type'] = SchoolAccommodationType.objects.filter(
                    ref_school=school_id).order_by("id")
                context['accommodation_service'] = SchoolAccommodationService.objects.filter(
                    ref_school=school_id).order_by("id")
                context['accommodation_owner'] = SchoolAccommodationOwner.objects.filter(
                    ref_school=school_id).order_by("id")
                context['service'] = SchoolService.objects.filter(
                    ref_school=school_id).order_by("-service_type")
                context['course'] = SchoolCourse.objects.filter(
                    ref_school=school_id)
                context['schedule'] = SchoolSchedule.objects.filter(
                    ref_school=school_id)
                context['rooms'] = SchoolRoom.objects.filter(
                    ref_school=school_id)
                context['level'] = SchoolCourseLevel.objects.filter(
                    ref_school=school_id)
                context['type'] = SchoolCourseType.objects.filter(
                    ref_school=school_id)
                context['teacher'] = TeacherUserProfile.objects.filter(
                    ref_school=school_id)
                context['students'] = SchoolStudentUserProfile.objects.filter(
                    ref_school=school_id)
                context['latters_type'] = SchoolLetterType.objects.filter(
                    ref_school=school_id)
                context['latters'] = SchoolLetter.objects.filter(
                    ref_type__ref_school=school_id)
                context['expenses'] = SchoolExpense.objects.filter(
                    ref_school=school_id)
                context['payrolls'] = SchoolPayroll.objects.filter(
                    ref_school=school_id)
                # Compare Two Dates, If Valid Upto Date Expire then set to "False"
                discounts = SchoolCourseDiscount.objects.filter(
                    ref_school=school_id)
                for discount in discounts:
                    if discount.valid_upto < current_day:
                        print('[*] Invalid Coupon')
                        discount.is_active = False
                        discount.save()
                context['discounts'] = discounts
                context['sponsors'] = SchoolSponsor.objects.filter(
                    ref_school=school_id)
                return context
            else:
                raise_permission_denied = True
            
        elif user.groups.filter(name='organization').exists():
            school_id = self.kwargs.get('pk', None)
            context = super(DetailSchool, self).get_context_data(**kwargs)

            context['application_form'] = DynamicSchoolApplicationFormField.objects.filter(ref_school=school_id)

            context['accommodation_type'] = SchoolAccommodationType.objects.filter(
                ref_school=school_id).order_by("id")
            context['accommodation_service'] = SchoolAccommodationService.objects.filter(ref_school=school_id).order_by("id")
            context['accommodation_owner'] = SchoolAccommodationOwner.objects.filter(
                ref_school=school_id).order_by("id")
            context['service'] = SchoolService.objects.filter(
                ref_school=school_id).order_by("-service_type")
            context['course'] = SchoolCourse.objects.filter(
                ref_school=school_id)
            context['schedule'] = SchoolSchedule.objects.filter(
                ref_school=school_id)
            context['rooms'] = SchoolRoom.objects.filter(ref_school=school_id)
            context['level'] = SchoolCourseLevel.objects.filter(
                ref_school=school_id)
            context['type'] = SchoolCourseType.objects.filter(
                ref_school=school_id)
            context['teacher'] = TeacherUserProfile.objects.filter(
                ref_school=school_id)
            context['students'] = SchoolStudentUserProfile.objects.filter(
                ref_school=school_id)
            context['latters_type'] = SchoolLetterType.objects.filter(
                ref_school=school_id)
            context['latters'] = SchoolLetter.objects.filter(
                ref_type__ref_school=school_id)
            context['sponsors'] = SchoolSponsor.objects.filter(
                ref_school=school_id)

            return context
        
        elif user.groups.filter(name='admin').exists():
            school_id = self.kwargs.get('pk', None)
            context = super(DetailSchool, self).get_context_data(**kwargs)
            context['accommodation_service'] = SchoolAccommodationService.objects.filter(ref_school=school_id).order_by("id")
            context['service'] = SchoolService.objects.filter(
                ref_school=school_id).order_by("-service_type")
            context['course'] = SchoolCourse.objects.filter(
                ref_school=school_id)
            context['application_form'] = DynamicSchoolApplicationFormField.objects.filter(ref_school=school_id)
            context['sponsors'] = SchoolSponsor.objects.filter(
                ref_school=school_id)
            return context
        
        elif user.is_superuser:
            school_id = self.kwargs.get('pk', None)
            context = super(DetailSchool, self).get_context_data(**kwargs)
            logged_in_user = user.is_superuser
            if logged_in_user:
                context['accommodation_type'] = SchoolAccommodationType.objects.filter(
                    ref_school=school_id).order_by("id")
                context['accommodation_service'] = SchoolAccommodationService.objects.filter(
                    ref_school=school_id).order_by("id")
                context['accommodation_owner'] = SchoolAccommodationOwner.objects.filter(
                    ref_school=school_id).order_by("id")
                context['service'] = SchoolService.objects.filter(
                    ref_school=school_id).order_by("-service_type")
                context['course'] = SchoolCourse.objects.filter(
                    ref_school=school_id)
                context['schedule'] = SchoolSchedule.objects.filter(
                    ref_school=school_id)
                context['rooms'] = SchoolRoom.objects.filter(
                    ref_school=school_id)
                context['level'] = SchoolCourseLevel.objects.filter(
                    ref_school=school_id)
                context['type'] = SchoolCourseType.objects.filter(
                    ref_school=school_id)
                context['teacher'] = TeacherUserProfile.objects.filter(
                    ref_school=school_id)
                context['students'] = SchoolStudentUserProfile.objects.filter(
                    ref_school=school_id)
                context['latters_type'] = SchoolLetterType.objects.filter(
                    ref_school=school_id)
                context['latters'] = SchoolLetter.objects.filter(
                    ref_type__ref_school=school_id)
                context['sponsors'] = SchoolSponsor.objects.filter(
                    ref_school=school_id)
            return context
        
        else:
            raise_permission_denied = True
        
        if raise_permission_denied:
            raise PermissionDenied()


'''def create_school_course_price(request, pk):
	course = SchoolCourse.objects.filter(pk=pk)
	course = course.first()
	context = {}

	#print(course.ref_school.id)

	PriceFormset = modelformset_factory(
	    SchoolCoursePrice, form=SchoolCoursePriceForm)
	formset = PriceFormset(request.POST or None, queryset= SchoolCourse.objects.none(
	), prefix='rel_ref_school_school_course')
	if request.method=='POST':
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
	return render(request, 'admin/master/course_price.html', context)'''


class EditSchoolCoursePrice(UpdateView):
    model = SchoolCoursePrice
    form_class = SchoolCoursePriceForm
    template_name = 'admin/master/edit_school_course_price.html'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:deatil_school', args=(self.object.ref_school_course.ref_school.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Edit'
        # context['event'] = event
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        messages.success(self.request, 'Successfully Update.')
        return super(EditSchoolCoursePrice, self).form_valid(form)


class DeleteSchoolCoursePrice(DeleteView):
    model = SchoolCoursePrice
    template_name = 'admin/master/delete_school_course_price.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:deatil_school', args=(self.object.ref_school_course.ref_school.id,))

    def get_context_data(self, **kwargs):
        school_course_price_id = self.kwargs.get('pk', None)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete'
        context['content'] = 'Are you sure you want to delete ?'
        return context


@login_required
@permission_required(['db.add_schoolservice'], raise_exception=True)
def create_school_service(request, pk):
    school = get_object_or_404(School, pk=pk)

    CHECK_USER_PERMISSION(request, school)

    # school = school.first()
    context = {}
    SchoolServiceFormset = modelformset_factory(
        SchoolService, form=SchoolServiceForm)
    service_formset = SchoolServiceFormset(
        request.POST or None, queryset=SchoolService.objects.none(), prefix='rel_ref_school_service')

    if request.method == 'POST':
        if service_formset.is_valid():
            try:
                with transaction.atomic():
                    for service in service_formset:
                        data = service.save(commit=False)
                        data.ref_school = school
                        data.save()
                return redirect('web:deatil_school', pk=school.id)
            except IntegrityError:
                error = "This data already exist"
                for theform in service_formset.forms:
                    theform.add_error(None, error)

    context['service_formset'] = service_formset
    context['school'] = school
    print(context)
    return render(request, 'admin/master/service/create_service.html', context)



class EditSchoolService(PermissionRequiredMixin, UpdateView):
    permission_required = ('db.change_schoolservice',)
    model = SchoolService
    form_class = SchoolServiceForm
    template_name = 'admin/master/service/edit_school_service.html'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:deatil_school', args=(self.object.ref_school.id,))

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Edit School Service'
        context['school'] = self.object.ref_school.id
        return context

    def form_valid(self, form):
        try:
            obj = form.save(commit=False)
            obj.user = self.request.user
            messages.success(self.request, 'Successfully Update.')
            return super(EditSchoolService, self).form_valid(form)
        except IntegrityError:
            error = "This data already exist"
            form.add_error(None, error)
            return self.render_to_response(self.get_context_data(form=form))


class DeleteSchoolService(PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_schoolservice',)
    model = SchoolService
    template_name = 'admin/master/service/delete_school_service.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:deatil_school', args=(self.object.ref_school.id,))

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        school_service_id = self.kwargs.get('pk', None)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Service'
        context['content'] = 'Are you sure you want to delete ?'
        context['school'] = self.object.ref_school.id
        return context


'''def create_school_accommodation_service(request, pk):
	school = School.objects.filter(pk=pk)
	school = school.first()
	context = {}
	SchoolAccommodationServiceFormset = modelformset_factory(
	    SchoolAccommodationService, form=SchoolAccommodationServiceForm)
	accommodation_service_formset = SchoolAccommodationServiceFormset(
	    request.POST or None, queryset= SchoolAccommodationService.objects.none(), prefix='rel_ref_school_accommodation_service')

	if request.method=='POST':
		if accommodation_service_formset.is_valid():
			try:
				with transaction.atomic():
					for service in accommodation_service_formset:
						data = service.save(commit=False)
						data.ref_school = school
						data.save()
			except IntegrityError:
				print("Error Encountered")
			return redirect('web:deatil_school', pk=school.id)

	context['accommodation_service_formset'] = accommodation_service_formset
	context['school'] = school
	return render(request, 'admin/master/create_accommodation_service.html', context)'''

'''class EditSchoolAccommodationService(UpdateView):
	model = SchoolAccommodationService
	form_class = SchoolAccommodationServiceForm
	template_name = 'admin/master/edit_accommodation_service.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:deatil_school', args=(self.object.ref_school.id,))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['title'] = 'Edit'
		#context['event'] = event
		return context

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		messages.success(self.request, 'Successfully Update.')
		return super(EditSchoolAccommodationService, self).form_valid(form)'''

'''class DeleteSchoolAccommodationService(DeleteView):
    model = SchoolAccommodationService
    template_name = 'admin/master/delete_accommodation_service.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:deatil_school', args=(self.object.ref_school.id,))

    def get_context_data(self, **kwargs):
    	school_service_id = self.kwargs.get('pk', None)
    	context = super().get_context_data(**kwargs)
    	context['title'] = 'Delete'
    	context['content'] = 'Are you sure you want to delete ?'
    	return context'''

# trasfer new folder course
'''def create_school_course(request, pk):
	school = School.objects.filter(pk=pk)
	school = school.first()
	context = {}
	PriceFormset = modelformset_factory(
	    SchoolCoursePrice, form=SchoolCoursePriceForm)
	form = SchoolCourseForm(request.POST or None)
	formset = PriceFormset(request.POST or None, queryset= SchoolCoursePrice.objects.none(
	), prefix='rel_ref_school_school_course')

	if request.method=='POST':
		if form.is_valid() and formset.is_valid():
			try:
				with transaction.atomic():
					course = form.save(commit=False)
					course.ref_school = school
					course.save()
					for price in formset:
						data = price.save(commit=False)
						data.ref_school_course = course
						data.save()
			except IntegrityError:
				print("Error Encountered")
			return redirect('web:deatil_school', pk=school.id)

	context['formset'] = formset
	context['school'] = school
	context['form'] = form
	return render(request, 'admin/master/create_school_course.html', context)'''

'''class SchoolCourseUpdateView(UpdateView):
    model = SchoolCourse
    form_class = SchoolCourseForm
    template_name = 'admin/master/create_school_course.html'
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
        instance = form.save()

        formset = self.PriceFormset(
            self.request.POST, prefix='rel_ref_school_school_course')
        if formset.is_valid():
            print('formset')
            total_forms = int(formset.data.get(
                'rel_ref_school_school_course-TOTAL_FORMS'))
            if total_forms > 0:
                SchoolCoursePrice.objects.filter(ref_school_course=self.object.id).delete()
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
        return super(SchoolCourseUpdateView, self).form_valid(form)'''


class DeleteSchoolCourse(PermissionRequiredMixin, DeleteView):
    permission_required = ('db.add_schoolcourse',)
    model = SchoolCourse
    template_name = 'admin/master/delete_school_course.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:deatil_school', args=(self.object.ref_school.id,))

    def get_context_data(self, **kwargs):
        # print(self.object.)
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        school_course_id = self.kwargs.get('pk', None)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete'
        context['content'] = 'Are you sure you want to delete ?'
        return context


@login_required
@permission_required(['db.add_schoolschedule'], raise_exception=True)
def create_school_schedule(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            school = School.objects.get(id=pk)
            if logged_in_user == school.id:
                data = request.POST.dict()
                form = SchoolScheduleForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        schedule = form.save(commit=False)
                        start_time = data.get('start_time')
                        end_time = data.get('end_time')
                        try:
                            schedule.ref_school = school
                            schedule.save()
                            print("Successfully add data")
                            return redirect('web:deatil_school', pk=school.id)
                        except IntegrityError:
                            error = f"This data already exist. {start_time} - {end_time}"
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'admin/master/schedule/create_school_schedule.html', {'form': form, 'school': school})
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists():
        try:
            school = School.objects.get(id=pk)
            if school.id:
                data = request.POST.dict()
                form = SchoolScheduleForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        schedule = form.save(commit=False)
                        start_time = data.get('start_time')
                        end_time = data.get('end_time')
                        try:
                            schedule.ref_school = school
                            schedule.save()
                            print("Successfully add data")
                            return redirect('web:deatil_school', pk=school.id)
                        except IntegrityError:
                            error = f"This data already exist. {start_time} - {end_time}"
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'admin/master/schedule/create_school_schedule.html', {'form': form, 'school': school})
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True

    elif user.is_superuser:
        try:
            school = School.objects.get(id=pk)
            if school.id:
                data = request.POST.dict()
                form = SchoolScheduleForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        schedule = form.save(commit=False)
                        start_time = data.get('start_time')
                        end_time = data.get('end_time')
                        try:
                            schedule.ref_school = school
                            schedule.save()
                            print("Successfully add data")
                            return redirect('web:deatil_school', pk=school.id)
                        except IntegrityError:
                            error = f"This data already exist. {start_time} - {end_time}"
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'admin/master/schedule/create_school_schedule.html', {'form': form, 'school': school})
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True
    else:
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()

@login_required
@permission_required(['db.change_schoolschedule'], raise_exception=True)
def edit_school_schedule(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            queryset = SchoolSchedule.objects.get(id=pk)
            if logged_in_user == queryset.ref_school.id:
                data = request.POST.dict()
                form = SchoolScheduleForm(instance=queryset)
                if request.method == 'POST':
                    form = SchoolScheduleForm(request.POST, instance=queryset)
                    if form.is_valid():
                        try:
                            form.save()
                            print("Successfully edit data")
                            return redirect('web:deatil_school', pk=queryset.ref_school.id)
                        except IntegrityError:
                            error = "This data already exist"
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = SchoolScheduleForm(instance=queryset)

                template_name = 'admin/master/schedule/edit_school_schedule.html'
                kwvars = {
                    'schedule': queryset,
                    'form': form,
                    'school': queryset.ref_school.id
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True
    
    elif user.groups.filter(name='teacher').exists():
        logged_in_user = request.user.teacheruserprofile.ref_school.id
        try:
            queryset = SchoolSchedule.objects.get(id=pk)
            if logged_in_user == queryset.ref_school.id:
                data = request.POST.dict()
                form = SchoolScheduleForm(instance=queryset)
                if request.method == 'POST':
                    form = SchoolScheduleForm(request.POST, instance=queryset)
                    if form.is_valid():
                        try:
                            form.save()
                            print("Successfully edit data")
                            return redirect('web:deatil_school', pk=queryset.ref_school.id)
                        except IntegrityError:
                            error = "This data already exist"
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = SchoolScheduleForm(instance=queryset)

                template_name = 'admin/master/schedule/edit_school_schedule.html'
                kwvars = {
                    'schedule': queryset,
                    'form': form,
                    'school': queryset.ref_school.id
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True

    elif user.groups.filter(name='teacher').exists() or user.is_superuser:
        try:
            queryset = SchoolSchedule.objects.get(id=pk)
            if queryset.ref_school.id:
                data = request.POST.dict()
                form = SchoolScheduleForm(instance=queryset)
                if request.method == 'POST':
                    form = SchoolScheduleForm(request.POST, instance=queryset)
                    if form.is_valid():
                        try:
                            form.save()
                            print("Successfully edit data")
                            return redirect('web:deatil_school', pk=queryset.ref_school.id)
                        except IntegrityError:
                            error = "This data already exist"
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = SchoolScheduleForm(instance=queryset)

                template_name = 'admin/master/schedule/edit_school_schedule.html'
                kwvars = {
                    'schedule': queryset,
                    'form': form,
                    'school': queryset.ref_school.id
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True
    
    else:
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()

@login_required
@permission_required(['db.delete_schoolschedule'], raise_exception=True)
def delete_school_schedule(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        print(logged_in_user)
        try:
            schedule = SchoolSchedule.objects.get(id=pk)
            _id = schedule.ref_school.id

            if logged_in_user == _id:
                if request.method == 'POST':
                    schedule.delete()
                    print("Delete Successfully")
                    return redirect('web:deatil_school', pk=schedule.ref_school.id)
                else:
                    pass
                return render(request, 'admin/master/schedule/delete_school_schedule.html', {'schedule': schedule, 'school': schedule.ref_school.id})
            else:
                print("==============================auth error===========")
                raise_permision_denied = True

        except:
            print("==============================try error===========")
            raise_permision_denied = True

    elif user.groups.filter(name='teacher').exists() or user.is_superuser:
        try:
            schedule = SchoolSchedule.objects.get(id=pk)
            _id = schedule.ref_school.id

            CHECK_USER_PERMISSION(request, schedule.ref_school)

            if _id:
                if request.method == 'POST':
                    schedule.delete()
                    print("Delete Successfully")
                    return redirect('web:deatil_school', pk=schedule.ref_school.id)
                else:
                    pass
                return render(request, 'admin/master/schedule/delete_school_schedule.html', {'schedule': schedule, 'school': schedule.ref_school.id})
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

@login_required
@permission_required(['db.add_schoolroom'], raise_exception=True)
def create_school_room(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            school = School.objects.get(id=pk)
            if logged_in_user == school.id:
                data = request.POST.dict()
                form = SchoolRoomForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        room = form.save(commit=False)
                        name = data.get('name')
                        capacity = data.get('capacity')
                        minimum = data.get('minimum')

                        # Checking capacity and minimum
                        if int(minimum) > int(capacity):
                            form.add_error(
                                None, 'Room Capacity Should not be less than Minimum')
                            return render(request, 'admin/master/room/create_school_room.html', {'form': form, 'school': school})

                        try:
                            room.ref_school = school
                            room.save()
                            print("Successfully add data")
                            return redirect('web:deatil_school', pk=school.id)
                        except IntegrityError:
                            error = f"Room Name : {str(name).title()}, this data already exist."
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'admin/master/room/create_school_room.html', {'form': form, 'school': school})
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True

    elif user.groups.filter(name='school').exists() or user.is_superuser:
        try:
            school = School.objects.get(id=pk)
            if school.id:
                data = request.POST.dict()
                form = SchoolRoomForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        room = form.save(commit=False)
                        name = data.get('name')
                        capacity = data.get('capacity')
                        minimum = data.get('minimum')

                        # Checking capacity and minimum
                        if int(minimum) > int(capacity):
                            form.add_error(
                                None, 'Room Capacity Should not be less than Minimum')
                            return render(request, 'admin/master/room/create_school_room.html', {'form': form, 'school': school})

                        try:
                            room.ref_school = school
                            room.save()
                            print("Successfully add data")
                            return redirect('web:deatil_school', pk=school.id)
                        except IntegrityError:
                            error = f"Room Name : {str(name).title()}, this data already exist."
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'admin/master/room/create_school_room.html', {'form': form, 'school': school})
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True

    else:
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.change_schoolroom'], raise_exception=True)
def edit_school_room(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            queryset = SchoolRoom.objects.get(id=pk)
            if logged_in_user == queryset.ref_school.id:
                data = request.POST.dict()
                form = SchoolRoomForm(instance=queryset)
                template_name = 'admin/master/room/edit_school_room.html'

                if request.method == 'POST':
                    form = SchoolRoomForm(request.POST, instance=queryset)
                    if form.is_valid():
                        capacity = data.get('capacity')
                        minimum = data.get('minimum')
                        name = data.get('name')

                        # Checking capacity and minimum
                        if int(minimum) > int(capacity):
                            form.add_error(
                                None, 'Room Capacity Should not be less than Minimum')
                        else:
                            try:
                                form.save()
                                print("Successfully edit data")
                                return redirect('web:deatil_school', pk=queryset.ref_school.id)
                            except IntegrityError:
                                error = f"Room Name : {str(name).title()}, this data already exist."
                                form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = SchoolRoomForm(instance=queryset)

                kwvars = {
                    'room': queryset,
                    'form': form,
                    'school': queryset.ref_school.id
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True
    
    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            queryset = SchoolRoom.objects.get(id=pk)
            if queryset.ref_school.id:
                data = request.POST.dict()
                form = SchoolRoomForm(instance=queryset)
                template_name = 'admin/master/room/edit_school_room.html'

                if request.method == 'POST':
                    form = SchoolRoomForm(request.POST, instance=queryset)
                    if form.is_valid():
                        capacity = data.get('capacity')
                        minimum = data.get('minimum')
                        name = data.get('name')

                        # Checking capacity and minimum
                        if int(minimum) > int(capacity):
                            form.add_error(
                                None, 'Room Capacity Should not be less than Minimum')
                        else:
                            try:
                                form.save()
                                print("Successfully edit data")
                                return redirect('web:deatil_school', pk=queryset.ref_school.id)
                            except IntegrityError:
                                error = f"Room Name : {str(name).title()}, this data already exist."
                                form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = SchoolRoomForm(instance=queryset)

                kwvars = {
                    'room': queryset,
                    'form': form,
                    'school': queryset.ref_school.id
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True
    
    else:
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.delete_schoolroom'], raise_exception=True)
def delete_school_room(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        print(logged_in_user)
        try:
            room = SchoolRoom.objects.get(id=pk)
            _id = room.ref_school.id

            if logged_in_user == _id:
                if request.method == 'POST':
                    room.delete()
                    print("Delete Successfully")
                    return redirect('web:deatil_school', pk=room.ref_school.id)
                else:
                    pass
                return render(request, 'admin/master/room/delete_school_room.html', {'room': room, 'school': room.ref_school.id})
            else:
                print("==============================auth error===========")
                raise_permision_denied = True

        except:
            print("==============================try error===========")
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            room = SchoolRoom.objects.get(id=pk)
            _id = room.ref_school.id

            if _id:
                if request.method == 'POST':
                    room.delete()
                    print("Delete Successfully")
                    return redirect('web:deatil_school', pk=room.ref_school.id)
                else:
                    pass
                return render(request, 'admin/master/room/delete_school_room.html', {'room': room, 'school': room.ref_school.id})
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


@login_required
@permission_required(['db.add_schoolcourselevel'], raise_exception=True)
def create_school_course_level(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            school = School.objects.get(id=pk)
            if logged_in_user == school.id:
                data = request.POST.dict()
                form = SchoolCourseLevelForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        level = form.save(commit=False)
                        name = data.get('name')
                        try:
                            level.ref_school = school
                            level.save()
                            print("Successfully add data")
                            return redirect('web:deatil_school', pk=school.id)
                        except IntegrityError:
                            error = f"Course Level: '{str(name).title()}' already exists."
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'admin/master/level/create_school_course_level.html', {'form': form, 'school': school})
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            school = School.objects.get(id=pk)
            if school.id:
                data = request.POST.dict()
                form = SchoolCourseLevelForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        level = form.save(commit=False)
                        name = data.get('name')
                        try:
                            level.ref_school = school
                            level.save()
                            print("Successfully add data")
                            return redirect('web:deatil_school', pk=school.id)
                        except IntegrityError:
                            error = f"Course Level: '{str(name).title()}' already exists."
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'admin/master/level/create_school_course_level.html', {'form': form, 'school': school})
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True
    
    else:
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.change_schoolcourselevel'], raise_exception=True)
def edit_school_course_level(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            queryset = SchoolCourseLevel.objects.get(id=pk)
            if logged_in_user == queryset.ref_school.id:
                data = request.POST.dict()
                form = SchoolCourseLevelForm(instance=queryset)
                if request.method == 'POST':
                    form = SchoolCourseLevelForm(
                        request.POST, instance=queryset)
                    if form.is_valid():
                        try:
                            form.save()
                            print("Successfully edit data")
                            return redirect('web:deatil_school', pk=queryset.ref_school.id)
                        except IntegrityError:
                            error = "This data already exists"
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = SchoolCourseLevelForm(instance=queryset)

                template_name = 'admin/master/level/edit_school_course_level.html'
                kwvars = {
                    'level': queryset,
                    'form': form,
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            queryset = SchoolCourseLevel.objects.get(id=pk)
            if queryset.ref_school.id:
                data = request.POST.dict()
                form = SchoolCourseLevelForm(instance=queryset)
                if request.method == 'POST':
                    form = SchoolCourseLevelForm(
                        request.POST, instance=queryset)
                    if form.is_valid():
                        try:
                            form.save()
                            print("Successfully edit data")
                            return redirect('web:deatil_school', pk=queryset.ref_school.id)
                        except IntegrityError:
                            error = "This data already exists"
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = SchoolCourseLevelForm(instance=queryset)

                template_name = 'admin/master/level/edit_school_course_level.html'
                kwvars = {
                    'level': queryset,
                    'form': form,
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True
    
    else:
        raise_permision_denied = True
    
    if raise_permision_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.delete_schoolcourselevel'], raise_exception=True)
def delete_school_course_level(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        print(logged_in_user)
        try:
            level = SchoolCourseLevel.objects.get(id=pk)
            _id = level.ref_school.id

            if logged_in_user == _id:
                if request.method == 'POST':
                    level.delete()
                    print("Delete Successfully")
                    return redirect('web:deatil_school', pk=level.ref_school.id)
                else:
                    pass
                return render(request, 'admin/master/level/delete_school_course_level.html', {'level': level})
            else:
                print("==============================auth error===========")
                raise_permision_denied = True

        except:
            print("==============================try error===========")
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            level = SchoolCourseLevel.objects.get(id=pk)
            _id = level.ref_school.id

            if _id:
                if request.method == 'POST':
                    level.delete()
                    print("Delete Successfully")
                    return redirect('web:deatil_school', pk=level.ref_school.id)
                else:
                    pass
                return render(request, 'admin/master/level/delete_school_course_level.html', {'level': level})
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


@login_required
@permission_required(['db.add_schoolcoursetype'], raise_exception=True)
def create_school_course_type(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            school = School.objects.get(id=pk)
            if logged_in_user == school.id:
                data = request.POST.dict()
                form = SchoolCourseTypeForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        coursetype = form.save(commit=False)
                        name = data.get('name')

                        try:
                            coursetype.ref_school = school
                            coursetype.save()
                            print("Successfully add data")
                            return redirect('web:deatil_school', pk=school.id)
                        except IntegrityError:
                            error = f"Course Type: '{str(name).title()}' already exists."
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'admin/master/coursetype/create_school_course_type.html', {'form': form, 'school': school})
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True
    
    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            school = School.objects.get(id=pk)
            if school.id:
                data = request.POST.dict()
                form = SchoolCourseTypeForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        coursetype = form.save(commit=False)
                        name = data.get('name')
                        try:
                            coursetype.ref_school = school
                            coursetype.save()
                            print("Successfully add data")
                            return redirect('web:deatil_school', pk=school.id)
                        except IntegrityError:
                            error = f"Course Type: '{str(name).title()}' already exists."
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'admin/master/coursetype/create_school_course_type.html', {'form': form, 'school': school})
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True
    
    else:
        raise_permision_denied = True
    
    if raise_permision_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.change_schoolcoursetype'], raise_exception=True)
def edit_school_course_type(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            queryset = SchoolCourseType.objects.get(id=pk)
            if logged_in_user == queryset.ref_school.id:
                data = request.POST.dict()
                form = SchoolCourseTypeForm(instance=queryset)
                if request.method == 'POST':
                    form = SchoolCourseTypeForm(
                        request.POST, instance=queryset)
                    if form.is_valid():
                        try:
                            form.save()
                            print("Successfully edit data")
                            return redirect('web:deatil_school', pk=queryset.ref_school.id)
                        except IntegrityError:
                            error = "This data already exists"
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = SchoolCourseTypeForm(instance=queryset)

                template_name = 'admin/master/coursetype/edit_school_course_type.html'
                kwvars = {
                    'coursetype': queryset,
                    'form': form,
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True
    
    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            queryset = SchoolCourseType.objects.get(id=pk)
            if queryset.ref_school.id:
                data = request.POST.dict()
                form = SchoolCourseTypeForm(instance=queryset)
                if request.method == 'POST':
                    form = SchoolCourseTypeForm(
                        request.POST, instance=queryset)
                    if form.is_valid():
                        try:
                            form.save()
                            print("Successfully edit data")
                            return redirect('web:deatil_school', pk=queryset.ref_school.id)
                        except IntegrityError:
                            error = "This data already exists"
                            form.add_error(None, error)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = SchoolCourseTypeForm(instance=queryset)

                template_name = 'admin/master/coursetype/edit_school_course_type.html'
                kwvars = {
                    'coursetype': queryset,
                    'form': form,
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except School.DoesNotExist:
            raise_permision_denied = True
    
    else:
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.delete_schoolcoursetype'], raise_exception=True)
def delete_school_course_type(request, pk):
    user = request.user
    raise_permision_denied = False
    
    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        # print(logged_in_user)
        try:
            coursetype = SchoolCourseType.objects.get(id=pk)
            _id = coursetype.ref_school.id

            if logged_in_user == _id:
                if request.method == 'POST':
                    coursetype.delete()
                    print("Delete Successfully")
                    return redirect('web:deatil_school', pk=coursetype.ref_school.id)
                else:
                    pass
                return render(request, 'admin/master/coursetype/delete_school_course_type.html', {'coursetype': coursetype})
            else:
                print("==============================auth error===========")
                raise_permision_denied = True

        except:
            print("==============================try error===========")
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:

        try:
            coursetype = SchoolCourseType.objects.get(id=pk)
            _id = coursetype.ref_school.id

            if _id:
                if request.method == 'POST':
                    coursetype.delete()
                    print("Delete Successfully")
                    return redirect('web:deatil_school', pk=coursetype.ref_school.id)
                else:
                    pass
                return render(request, 'admin/master/coursetype/delete_school_course_type.html', {'coursetype': coursetype})
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


@login_required
def create_dynamic_school_application_form_field(request, pk):
    school = School.objects.filter(pk=pk)
    school = school.first()
    context = {}
    DynamicSchoolApplicationFormFieldFormset = modelformset_factory(
        DynamicSchoolApplicationFormField, form=DynamicSchoolApplicationFormFieldForm)
    formset = DynamicSchoolApplicationFormFieldFormset(
        request.POST or None, queryset=DynamicSchoolApplicationFormField.objects.none(), prefix='rel_ref_school_school_application_form')

    if request.method == 'POST':
        if formset.is_valid():
            try:
                with transaction.atomic():
                    for application in formset:
                        data = application.save(commit=False)
                        data.ref_school = school
                        data.save()
            except IntegrityError:
                print("Error Encountered")
            return redirect('web:deatil_school', pk=school.id)

    context['formset'] = formset
    context['school'] = school
    return render(request, 'admin/master/create_dynamic_school_application_form_field.html', context)


def get_city(request):
    country_id = request.GET.get('country')
    if country_id:
        cities = City.objects.filter(
            ref_country=country_id).order_by('city_name')
        return render(request, 'admin/master/city_dropdown_list_options.html', {'cities': cities})
    else:
        return render(request, 'admin/master/city_dropdown_list_options_emty.html')


def get_schools(request):
    city_id = request.GET.get('city')
    if city_id:
        schools = School.objects.filter(
            ref_city=city_id).order_by('school_name')
        return render(request, 'admin/master/school_dropdown_list_options.html', {'schools': schools})
    else:
        return render(request, 'admin/master/school_dropdown_list_options_emty.html')


def get_school_address(request):
    school_id = request.GET.get('school')

    if school_id:
        school = get_object_or_404(School, pk=school_id)
        school_address = school.school_address
        output = f"Email: {school.email} <br>Address: {school_address}"
        return HttpResponse(output)
    else:
        return HttpResponse('')


def get_available_teachers_and_rooms(request,):
    school = request.GET.get('school', None)
    schedule = request.GET.get('schedule', None)
    minimum = request.GET.get('minimum', None)
    maximum = request.GET.get('maximum', None)
    days = request.GET.getlist('days[]', None)

    # User.objects.get(id=self.ref_teacher_name.id).
    available_teachers = TeacherUserProfile.objects.filter(
        ref_school_id=school
    ).exclude(
        ref_user_id__in=SchoolClass.objects.filter(
            ref_schedule_id=schedule,
            ref_day__in=days,
        ).values_list('ref_teacher_name', flat=True)
    )

    available_rooms = SchoolRoom.objects.filter(
        ref_school_id=school,
        capacity__gte=maximum,
        minimum__lte=minimum,
    ).exclude(
        id__in=SchoolClass.objects.filter(
            ref_schedule_id=schedule,
            ref_day__in=days,
        ).values_list('ref_room_id', flat=True)
    )

    # Convert the queryset to a list of dictionaries
    available_teachers_list = list(available_teachers.values())
    available_rooms_list = list(available_rooms.values())

    # Create a dictionary with the available teachers and rooms
    response_dict = {
        'available_rooms': available_rooms_list,
        'available_teachers': available_teachers_list,
    }

    # Convert the dictionary to JSON and return as a response
    return JsonResponse(response_dict)


def get_school_for_org(request):
    organization_id = request.GET.get('organization')
    print("==============================================================")
    print(organization_id)
    if organization_id:
        schools = School.objects.filter(
            ref_organization=organization_id).order_by('school_name')
        return render(request, 'admin/master/school_dropdown_list_options.html', {'schools': schools})
    else:
        return render(request, 'admin/master/school_dropdown_list_options_emty.html')


def get_course_ajax(request):
    schools_id = request.GET.get('school')
    if schools_id:
        coureses = SchoolCourse.objects.filter(
            ref_school=schools_id).order_by('title')
        return render(request, 'admin/master/course_dropdown_list_options.html', {'coureses': coureses})
    else:
        return render(request, 'admin/master/course_dropdown_list_options_emty.html')


def get_course_type_ajax(request):
    schools_id = request.GET.get('school')
    if schools_id:
        course_types = SchoolCourseType.objects.filter(
            ref_school=schools_id).order_by('name')
        return render(request, 'admin/master/course_type_dropdown_list_options.html', {'course_types': course_types})
    else:
        return render(request, 'admin/master/course_type_dropdown_list_options_emty.html')


def get_user_role(request):
    role = None
    try:
        user = request.user
        if user.is_superuser:
            role = "admin"
        else:
            roles = user.groups.filter().all()
            for _role in roles:
                role = _role.name
    except Exception as e:
        pass
    return role


def get_course_class_ajax(request):

    schools_id = request.GET.get('school')
    course_id = request.GET.get('course')
    course_type_id = request.GET.get('course_type')

    role = get_user_role(request)
    can_apply = True

    if schools_id and course_id and course_type_id:

        if role == 'student':
            # Student User can't apply for course in multiple locations
            _course = get_object_or_404(SchoolCourse, pk=course_id)

            active_courses = Application.objects.filter(
                user=request.user, ap_end_date__gte=timezone.now().date(), ap_status=1)

            if active_courses:
                for _act in active_courses:
                    if _act.ref_school.id == int(schools_id):
                        can_apply = True
                    else:
                        can_apply = False
                    print(_act.ref_school.id)

                if not can_apply:
                    return render(request, 'admin/master/can_not_apply_emty.html', {'active_courses': active_courses})

        coureses = SchoolClass.objects.filter(
            ref_school=schools_id, ref_course=course_id, ref_type_of_course=course_type_id, summar_end__gte=timezone.now().date()).order_by('title')
        return render(request, 'admin/master/class_dropdown_list_options.html', {'coureses': coureses})
    else:
        return render(request, 'admin/master/class_dropdown_list_options_emty.html')


def get_exams_ajax(request):

    schools_id = request.GET.get('school')
    course_id = request.GET.get('course')

    role = get_user_role(request)

    if schools_id and course_id:

        if role == 'school':
            _course = get_object_or_404(SchoolClass, pk=course_id)

            exams = SchoolExam.objects.filter(
                ref_exam_type__name="Intermediate", ref_course=_course)

        return render(request, 'admin/master/exam_dropdown_list_options.html', {'exams': exams})
    else:
        return render(request, 'admin/master/exam_dropdown_list_options_empty.html')


def get_exams_ajax(request):

    schools_id = request.GET.get('school')
    course_id = request.GET.get('course')

    role = get_user_role(request)

    if schools_id and course_id:

        if role == 'school':
            _course = get_object_or_404(SchoolClass, pk=course_id)
            
            exams = SchoolExam.objects.filter(
                ref_exam_type__name="Level Up", ref_course=_course)
            print(exams)

        return render(request, 'admin/master/exam_dropdown_list_options.html', {'exams': exams})
    else:
        return render(request, 'admin/master/exam_dropdown_list_options_empty.html')


def get_students_ajax(request):

    schools_id = request.GET.get('school')
    course_id = request.GET.get('course')

    role = get_user_role(request)

    if schools_id and course_id:

        if role == 'school':
            _course = get_object_or_404(SchoolClass, pk=course_id)

            students = StudentProfileHasCourse.objects.filter(
                ref_student__ref_school__pk=schools_id, ref_course=_course)

        return render(request, 'admin/master/student_dropdown_list_options.html', {'students': students})
    else:
        return render(request, 'admin/master/student_dropdown_list_options_empty.html')


def get_course_end_date_ajax(request):

    schools_id = request.GET.get('school')
    course_id = request.GET.get('course')

    role = get_user_role(request)

    if schools_id and course_id:
        if role == 'school':
            _course = get_object_or_404(SchoolClass, pk=course_id)
            return JsonResponse({'end_date': _course.summar_end})

        return JsonResponse({'end_date': timezone.now().date()})


def get_course_class_days_ajax(request):
    course_id = request.GET.get('course')

    if course_id:
        coureses = get_object_or_404(SchoolClass, pk=course_id)
        course_days = coureses.ref_day_list
        course_start_day = coureses.start_day
        class_days = []

        if course_start_day:
            if course_start_day == 'Sunday':
                class_days.append(0)
            elif course_start_day == 'Monday':
                class_days.append(1)
            elif course_start_day == 'Tuesday':
                class_days.append(2)
            elif course_start_day == 'Wednesday':
                class_days.append(3)
            elif course_start_day == 'Thursday':
                class_days.append(4)
            elif course_start_day == 'Friday':
                class_days.append(5)
            elif course_start_day == 'Saturday':
                class_days.append(6)
        else:

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

        # print(coureses.ref_day)
        return JsonResponse({'start_date': coureses.summar_start, 'end_date': coureses.summar_end, 'days': class_days})
    else:
        return JsonResponse({'start_date': '', 'end_date': '', 'days': []})


def get_course_class_price_ajax(request):
    course_class_id = request.GET.get('course_class')

    role = get_user_role(request)

    if role == 'student' and course_class_id:
        # Student User can't apply for diffrent course same days
        can_apply = True
        active_classes = []
        class_days = []

        _class = get_object_or_404(SchoolClass, pk=course_class_id)
        current_class_days = str(_class.ref_day_list).split(', ')
        print(current_class_days)

        active_courses = Application.objects.filter(ref_school=_class.ref_school,
                                                    user=request.user, ap_end_date__gte=timezone.now().date())

        for active_course in active_courses.values_list('ap_course_class'):
            if active_course[-1]:
                active_classes.append(active_course[-1])

        school_class = SchoolClass.objects.filter(id__in=active_classes)

        for _s_class in school_class:
            __days = str(_s_class.ref_day_list).split(', ')
            for _day in __days:
                class_days.append(_day)

        print(class_days)
        for c_day in current_class_days:
            if c_day in class_days:
                can_apply = False
                break

        if not can_apply:
            return render(request, 'admin/master/can_not_apply.html', {'school_class': school_class})

    if course_class_id:
        price_list = SchoolCoursePrice.objects.filter(
            ref_school_course=course_class_id).order_by('min_weak')
        if price_list:
            return render(request, 'admin/master/course_price_list_ajax.html', {'price_list': price_list})
    else:
        return render(request, 'admin/master/course_price_ajax_emty.html')


def get_study_period_ajax(request):
    course_class_id = request.GET.get('course_class')
    if course_class_id:
        price_list = SchoolCoursePrice.objects.filter(
            ref_school_course=course_class_id).order_by('min_weak')
        if price_list:
            # Checking course study period
            course = price_list.first().ref_school_course.title
            course_start = price_list.first().ref_school_course.summar_start
            course_end = price_list.first().ref_school_course.summar_end
            current_date = timezone.now().date()

            if current_date > course_start:
                print('='*30)
                print(f'[*] Current date is greater than course start date.\nCourse: {course}\nCurrent Date: {current_date}\nTimeline {course_start} : {course_end}')
                print('='*30)
                course_days = (course_end - current_date).days
            else:
                print('='*30)
                print(f'[*] Current date is less than course start date.\nCourse: {course}\nCurrent Date: {current_date}\nTimeline {course_start} : {course_end}')
                print('='*30)
                course_days = (course_end - course_start).days

            # End checking course study period

            # for price in price_list:
            #     for week in range(price.min_weak, price.max_weak + 1):
            #         study_periods.append(week)

            course_weeks = int(course_days / 7)
            if not course_days % 7 == 0:
                course_weeks += 1

            study_periods = [week for week in range(1, course_weeks + 1)]
            print(f'[*] Course Days: {course_days}, Course Weeks: {course_weeks}')

            
            return render(request, 'admin/master/study_period_dropdown_list_options.html', {'study_periods': study_periods})
    else:
        return render(request, 'admin/master/study_period_dropdown_list_options_empty.html')


def get_accommodation_type_ajax(request):
    schools_id = request.GET.get('school')
    if schools_id:
        acco_types = SchoolAccommodationOwner.objects.filter(
            ref_school=schools_id).order_by('accommodation_type').distinct('accommodation_type')

        return render(request, 'admin/master/acc_type_dropdown_list_options.html', {'acco_types': acco_types})
    else:
        return render(request, 'admin/master/acc_type_dropdown_list_empty.html')


def get_level_ajax(request):
    schools_id = request.GET.get('school')
    if schools_id:
        level = SchoolCourseLevel.objects.filter(
            ref_school=schools_id).order_by('name')
        return render(request, 'admin/master/level_dropdown_list_options.html', {'level': level})
    else:
        return render(request, 'admin/master/level_dropdown_list_options_emty.html')


def get_service_ajax(request):
    schools_id = request.GET.get('school')
    if schools_id:
        services = SchoolService.objects.filter(
            ref_school=schools_id).order_by('service_type')

        return render(request, 'admin/master/service_dropdown_list_options.html', {'services': services})
    else:
        return render(request, 'admin/master/service_dropdown_list_options_emty.html')


def get_accommodation_ajax(request):
    schools_id = request.GET.get('school')
    acco_type = request.GET.get('acco_type')

    if schools_id and acco_type:
        accommodation = SchoolAccommodationService.objects.filter(
            ref_school=schools_id, ref_accommodation_owner__accommodation_type=acco_type, status=True).order_by('id')

        # For Manual Accommodation
        if acco_type == '-1':
            return render(request, 'admin/master/manual_accommodation_dropdown_list_options.html', {'acco_type': acco_type})
        else:
            return render(request, 'admin/master/accommodation_dropdown_list_options.html', {'accommodation': accommodation})
    else:
        return render(request, 'admin/master/accommodation_dropdown_list_options_emty.html')


def get_course_discount(request):
    course_id = request.GET.get('course')
    school_id = request.GET.get('school')

    if course_id:
        discounts = SchoolCourseDiscount.objects.filter(
            ref_course=course_id, ref_school_id=school_id, is_active=True, valid_from__lte=current_day, valid_upto__gte=current_day)
        if discounts:
            return render(request, 'admin/master/course_discount_dropdown_list_options.html', {'discounts': discounts})

    return render(request, 'admin/master/course_discount_dropdown_list_options_empty.html')


def get_course_price_ajax(request):
    course_id = request.GET.get('course')
    period_id = request.GET.get('period')

    if course_id and period_id:
        price = SchoolCoursePrice.objects.filter(
            ref_school_course=course_id, min_weak__lte=period_id, max_weak__gte=period_id)

        if price:
            return render(request, 'admin/master/course_price_ajax.html', {'price': price})

        else:
            return render(request, 'admin/master/course_price_ajax.html', {'error': "Note: Your  selected Study period did not match price list"})

    elif course_id:
        price_list = SchoolCoursePrice.objects.filter(
            ref_school_course=course_id).order_by('min_weak')
        if price_list:
            return render(request, 'admin/master/course_price_list_ajax.html', {'price_list': price_list})
        else:
            return render(request, 'admin/master/course_price_ajax_emty.html')

    # elif period_id:
    #     # return render(request, 'admin/master/course_price_list_ajax.html', {'error':"Please select Course"})
    #     discount_list_html = [
    #         '<option value="" selected="">---------</option>']
    #     price_list_html = render_to_string(
    #         'admin/master/course_price_list_ajax.html', {'error': "Please select Course"})
    #     return JsonResponse({'price_list_html': price_list_html, 'discount_list_html': discount_list_html, "class_days_list": class_days_list, 'course_min_week': -1, 'course_max_week': -1})
    else:
        return render(request, 'admin/master/course_price_ajax_emty.html')
