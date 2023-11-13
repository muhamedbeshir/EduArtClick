from datetime import date, timedelta
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from v1.db.master.school import School
from v1.db.school.school_setting import SchoolSetting
from v1.web.utils import CHECK_USER_PERMISSION
from v1.web.views.admin.master.school.setting import SchoolSettingForm
from v1.base.configs import cRequest
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError



class SchoolSettingCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('db.add_schoolsetting',)
    model = SchoolSetting
    form_class = SchoolSettingForm
    template_name = 'admin/school/setting/add_school_setting.html'

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        cRequest.params[ "school_id" ] = kwargs.get( "pk" )
        school_id = kwargs.get( "pk" )
        school = get_object_or_404(School, pk=school_id)
        CHECK_USER_PERMISSION(self.request, school)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('web:list_school_setting', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add School Setting"
        context['school'] = cRequest.params[ "school_id" ]
        cRequest.params[ "school_id" ] = context['school']
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)

        school_id = cRequest.params[ "school_id" ]
        cRequest.params[ "school_id" ] = school_id
        try:
            school = get_object_or_404(School, pk=school_id)
            obj.ref_school = school
            messages.success(self.request, 'Successfully Added.')
            return super(__class__, self).form_valid(form)
        except IntegrityError:
            error = 'You can not add more than one'
            form.add_error(None, error)
        
        return super(__class__, self).form_invalid(form)


class SchoolSettingEditView(PermissionRequiredMixin, UpdateView):
    permission_required = ('db.change_schoolsetting',)
    model = SchoolSetting
    form_class = SchoolSettingForm
    template_name = 'admin/school/setting/add_school_setting.html'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:list_school_setting', args=(self.object.ref_school.id,))

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
		
        context['title'] = 'Edit School Setting'
        context['school'] = self.object.ref_school.id
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)

        school_id = self.object.ref_school.id
        cRequest.params[ "school_id" ] = school_id
        try:
            school = get_object_or_404(School, pk=school_id)
            obj.ref_school = school
            messages.success(self.request, 'Successfully Added.')
            return super(__class__, self).form_valid(form)
        except IntegrityError:
            error = 'You can not add more than one'
            form.add_error(None, error)
        
        return super(__class__, self).form_invalid(form)


class SchoolSettingListView(PermissionRequiredMixin, ListView):
    permission_required = ('db.view_schoolsetting',)
    model = SchoolSetting
    context_object_name = 'applications'
    template_name = 'admin/school/setting/school_setting_list.html'
    #ordering = ['-id']
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        cRequest.params[ "school_id" ] = kwargs.get( "pk" )
        school_id = kwargs.get( "pk" )
        school = get_object_or_404(School, pk=school_id)
        CHECK_USER_PERMISSION(self.request, school)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "School Setting List"
        context['school'] = cRequest.params[ "school_id" ]
        cRequest.params[ "school_id" ] = context['school']
        return context


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
        print('<=>'*10, role)
        # if (role == "aggent"):
        #     queryset = SchoolSetting.objects.filter(user=self.request.user).order_by("-id")
        # elif (role == "student"):
        queryset = SchoolSetting.objects.filter(ref_school=cRequest.params[ "school_id" ]).order_by("-id")
        return queryset
    

class SchoolSettingDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_schoolsetting',)
    model = SchoolSetting
    template_name = 'admin/school/setting/school_setting_delete.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:dashboard')

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        school_id = self.kwargs.get('pk', None)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete School Setting'
        context['content'] = 'Are you sure you want to delete ?'
        return context