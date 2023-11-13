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


@login_required
@permission_required(['db.add_useraddress'], raise_exception=True)
def create_teacher_user_address_by_school(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            user = User.objects.get(id=pk)
            _id = user.teacheruserprofile.ref_school.id

            if logged_in_user == _id:
                data = request.POST.dict()
                form = UserAddressForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        address = form.save(commit=False)
                        street_1 = data.get('street_1')
                        street_2 = data.get('street_2')
                        city = data.get('city')
                        state = data.get('state')
                        code = data.get('code')
                        address.ref_user = user
                        address.save()
                        print("Successfully add data")
                        return redirect('web:school_teacher_detail', pk=address.ref_user.teacheruserprofile.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'auth/address/create_teacher_user_address_by_school.html', {'teacher': user.teacheruserprofile.id, 'form': form})
            else:
                print("============Error===================")
                raise_permision_denied = True
        except User.DoesNotExist:
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            user = User.objects.get(id=pk)
            _id = user.teacheruserprofile.ref_school.id

            if _id:
                data = request.POST.dict()
                form = UserAddressForm(request.POST or None)
                if request.method == 'POST':
                    if form.is_valid():
                        address = form.save(commit=False)
                        street_1 = data.get('street_1')
                        street_2 = data.get('street_2')
                        city = data.get('city')
                        state = data.get('state')
                        code = data.get('code')
                        address.ref_user = user
                        address.save()
                        print("Successfully add data")
                        return redirect('web:school_teacher_detail', pk=address.ref_user.teacheruserprofile.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    pass

                return render(request, 'auth/address/create_teacher_user_address_by_school.html', {'teacher': user.teacheruserprofile.id, 'form': form})
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
@permission_required(['db.change_useraddress'], raise_exception=True)
def edit_teacher_user_address_by_school(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            queryset = UserAddress.objects.get(id=pk)
            _id = queryset.ref_user.teacheruserprofile.ref_school.id

            if logged_in_user == _id:
                data = request.POST.dict()
                form = UserAddressForm(instance=queryset)
                if request.method == 'POST':
                    form = UserAddressForm(request.POST, instance=queryset)
                    if form.is_valid():
                        form.save()
                        print("Successfully update data")
                        return redirect('web:school_teacher_detail', pk=queryset.ref_user.teacheruserprofile.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = UserAddressForm(instance=queryset)
                template_name = 'auth/address/edit_teacher_user_address_by_school.html'
                kwvars = {
                    'address': queryset,
                    'form': form,
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except UserAddress.DoesNotExist:
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            queryset = UserAddress.objects.get(id=pk)
            _id = queryset.ref_user.teacheruserprofile.ref_school.id

            if _id:
                data = request.POST.dict()
                form = UserAddressForm(instance=queryset)
                if request.method == 'POST':
                    form = UserAddressForm(request.POST, instance=queryset)
                    if form.is_valid():
                        form.save()
                        print("Successfully update data")
                        return redirect('web:school_teacher_detail', pk=queryset.ref_user.teacheruserprofile.id)
                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)
                else:
                    form = UserAddressForm(instance=queryset)
                template_name = 'auth/address/edit_teacher_user_address_by_school.html'
                kwvars = {
                    'address': queryset,
                    'form': form,
                }

                return render(request, template_name, kwvars)
            else:
                raise_permision_denied = True
        except UserAddress.DoesNotExist:
            raise_permision_denied = True
    else:
        raise_permision_denied = True

    if raise_permision_denied:
        raise PermissionDenied()


@login_required
@permission_required(['db.delete_useraddress'], raise_exception=True)
def delete_teacher_user_address_by_school(request, pk):
    user = request.user
    raise_permision_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        print(logged_in_user)
        try:
            address = UserAddress.objects.get(id=pk)
            _id = address.ref_user.teacheruserprofile.ref_school.id

            if logged_in_user == _id:
                if request.method == 'POST':
                    address.delete()
                    print("Delete Successfully")
                    return redirect('web:school_teacher_detail', pk=address.ref_user.teacheruserprofile.id)
                else:
                    pass
                return render(request, 'auth/address/delete_teacher_user_address_by_school.html', {'address': address})
            else:
                print("==============================auth error===========")
                raise_permision_denied = True

        except:
            print("==============================try error===========")
            raise_permision_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            address = UserAddress.objects.get(id=pk)
            _id = address.ref_user.teacheruserprofile.ref_school.id

            if _id:
                if request.method == 'POST':
                    address.delete()
                    print("Delete Successfully")
                    return redirect('web:school_teacher_detail', pk=address.ref_user.teacheruserprofile.id)
                else:
                    pass
                return render(request, 'auth/address/delete_teacher_user_address_by_school.html', {'address': address})
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
