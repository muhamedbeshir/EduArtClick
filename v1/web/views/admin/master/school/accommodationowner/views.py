from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Max
from django.core.exceptions import PermissionDenied

from v1.db.models import *
from v1.web.utils import CHECK_USER_PERMISSION

from .forms import *

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError


@login_required
@permission_required(['db.add_schoolaccommodationowner'], raise_exception=True)
def create_school_accommodation_owner(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            school = School.objects.get(id=pk)
            if logged_in_user == school.id:
                school = School.objects.filter(pk=pk)
                school = school.first()
                context = {}
                form = SchoolAccommodationOwnerForm(request.POST or None)
                data = request.POST.dict()
                if request.method == 'POST':
                    if form.is_valid():
                        accommodation_owner = form.save(commit=False)
                        type_id = accommodation_owner.accommodation_type
                        # print(type(type_id))
                        if accommodation_owner.accommodation_type == 0:
                            if accommodation_owner.first_name and accommodation_owner.last_name:
                                capacity_value = 11
                                capacity_input_value = int(
                                    accommodation_owner.capacity)
                                if (capacity_value > capacity_input_value):
                                    accommodation_owner.ref_school = school
                                    accommodation_owner.save()
                                    if accommodation_owner.capacity:
                                        capacity_count = int(
                                            accommodation_owner.capacity)

                                        res = []
                                        arr = [
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 1",
                                                                       price="0.0", code=1, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 2",
                                                                       price="0.0", code=2, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 3",
                                                                       price="0.0", code=3, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 4",
                                                                       price="0.0", code=4, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 5",
                                                                       price="0.0", code=5, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 6",
                                                                       price="0.0", code=6, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 7",
                                                                       price="0.0", code=7, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 8",
                                                                       price="0.0", code=8, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 9",
                                                                       price="0.0", code=9, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 10",
                                                                       price="0.0", code=10, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1)
                                        ]
                                        for item in arr:
                                            if (item.code <= capacity_count):
                                                res.append(item)
                                                print(res)
                                        try:
                                            SchoolAccommodationService.objects.bulk_create(
                                                res)
                                        except:
                                            print(
                                                "==================SchoolAccommodationService Not craete")
                                    else:
                                        pass
                                    return redirect('web:create_school_accommodation_owner_next_page_room', pk=accommodation_owner.id)
                                else:
                                    print("Form is not valid")
                                    error = "Capacity will be highest no 10"
                                    form.add_error(None, error)
                            else:
                                error = "First name and last is required!"
                                form.add_error(None, error)

                        elif accommodation_owner.accommodation_type == 1:
                            if accommodation_owner.company_name:
                                capacity_value = 101
                                capacity_input_value = int(
                                    accommodation_owner.capacity)
                                if (capacity_value > capacity_input_value):
                                    accommodation_owner.ref_school = school
                                    accommodation_owner.save()
                                    if accommodation_owner.capacity:
                                        capacity_count = int(
                                            accommodation_owner.capacity)

                                        res = []
                                        arr = [
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 1",
                                                                       price="0.0", code=1, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 2",
                                                                       price="0.0", code=2, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 3",
                                                                       price="0.0", code=3, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 4",
                                                                       price="0.0", code=4, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 5",
                                                                       price="0.0", code=5, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 6",
                                                                       price="0.0", code=6, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 7",
                                                                       price="0.0", code=7, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 8",
                                                                       price="0.0", code=8, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 9",
                                                                       price="0.0", code=9, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 10",
                                                                       price="0.0", code=10, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 11",
                                                                       price="0.0", code=11, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 12",
                                                                       price="0.0", code=12, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 13",
                                                                       price="0.0", code=13, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 14",
                                                                       price="0.0", code=14, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 15",
                                                                       price="0.0", code=15, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 16",
                                                                       price="0.0", code=16, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 17",
                                                                       price="0.0", code=17, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 18",
                                                                       price="0.0", code=18, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 19",
                                                                       price="0.0", code=19, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 20",
                                                                       price="0.0", code=20, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 21",
                                                                       price="0.0", code=21, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 22",
                                                                       price="0.0", code=22, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 23",
                                                                       price="0.0", code=23, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 24",
                                                                       price="0.0", code=25, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 25",
                                                                       price="0.0", code=25, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 26",
                                                                       price="0.0", code=26, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 27",
                                                                       price="0.0", code=27, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 28",
                                                                       price="0.0", code=28, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 29",
                                                                       price="0.0", code=29, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 30",
                                                                       price="0.0", code=30, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 31",
                                                                       price="0.0", code=31, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 32",
                                                                       price="0.0", code=32, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 33",
                                                                       price="0.0", code=33, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 34",
                                                                       price="0.0", code=34, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 35",
                                                                       price="0.0", code=35, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 36",
                                                                       price="0.0", code=36, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 37",
                                                                       price="0.0", code=37, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 38",
                                                                       price="0.0", code=38, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 39",
                                                                       price="0.0", code=39, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 40",
                                                                       price="0.0", code=40, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 41",
                                                                       price="0.0", code=41, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 42",
                                                                       price="0.0", code=42, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 43",
                                                                       price="0.0", code=43, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 44",
                                                                       price="0.0", code=44, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 45",
                                                                       price="0.0", code=45, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 46",
                                                                       price="0.0", code=46, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 47",
                                                                       price="0.0", code=47, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 48",
                                                                       price="0.0", code=48, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 49",
                                                                       price="0.0", code=49, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 50",
                                                                       price="0.0", code=50, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 51",
                                                                       price="0.0", code=51, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 52",
                                                                       price="0.0", code=52, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 53",
                                                                       price="0.0", code=53, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 54",
                                                                       price="0.0", code=54, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 55",
                                                                       price="0.0", code=55, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 56",
                                                                       price="0.0", code=56, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 57",
                                                                       price="0.0", code=57, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 58",
                                                                       price="0.0", code=58, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 59",
                                                                       price="0.0", code=59, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 60",
                                                                       price="0.0", code=60, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 61",
                                                                       price="0.0", code=61, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 62",
                                                                       price="0.0", code=62, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 63",
                                                                       price="0.0", code=63, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 64",
                                                                       price="0.0", code=64, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 65",
                                                                       price="0.0", code=65, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 66",
                                                                       price="0.0", code=66, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 67",
                                                                       price="0.0", code=67, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 68",
                                                                       price="0.0", code=68, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 69",
                                                                       price="0.0", code=69, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 70",
                                                                       price="0.0", code=70, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 71",
                                                                       price="0.0", code=71, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 72",
                                                                       price="0.0", code=72, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 73",
                                                                       price="0.0", code=73, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 74",
                                                                       price="0.0", code=74, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 75",
                                                                       price="0.0", code=75, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 76",
                                                                       price="0.0", code=76, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 77",
                                                                       price="0.0", code=77, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 78",
                                                                       price="0.0", code=78, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 79",
                                                                       price="0.0", code=79, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 80",
                                                                       price="0.0", code=80, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 81",
                                                                       price="0.0", code=81, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 82",
                                                                       price="0.0", code=82, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 83",
                                                                       price="0.0", code=83, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 84",
                                                                       price="0.0", code=84, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 85",
                                                                       price="0.0", code=85, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 86",
                                                                       price="0.0", code=86, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 87",
                                                                       price="0.0", code=87, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 88",
                                                                       price="0.0", code=88, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 89",
                                                                       price="0.0", code=89, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 90",
                                                                       price="0.0", code=90, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 91",
                                                                       price="0.0", code=91, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 92",
                                                                       price="0.0", code=92, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 93",
                                                                       price="0.0", code=93, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 94",
                                                                       price="0.0", code=94, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 95",
                                                                       price="0.0", code=95, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 96",
                                                                       price="0.0", code=96, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 97",
                                                                       price="0.0", code=97, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 98",
                                                                       price="0.0", code=98, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 99",
                                                                       price="0.0", code=99, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 100",
                                                                       price="0.0", code=100, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                        ]
                                        for item in arr:
                                            if (item.code <= capacity_count):
                                                res.append(item)
                                                print(res)
                                        try:
                                            SchoolAccommodationService.objects.bulk_create(
                                                res)
                                        except:
                                            print(
                                                "==================SchoolAccommodationService Not craete")
                                    else:
                                        pass
                                    return redirect('web:create_school_accommodation_owner_next_page_room', pk=accommodation_owner.id)
                                else:
                                    print("Form is not valid")
                                    error = "Capacity will be highest no 100"
                                    form.add_error(None, error)
                            else:
                                error = "Resident name required!"
                                form.add_error(None, error)
                        elif accommodation_owner.accommodation_type == 2:
                            if accommodation_owner.company_name:
                                capacity_value = 101
                                capacity_input_value = int(
                                    accommodation_owner.capacity)
                                if (capacity_value > capacity_input_value):
                                    accommodation_owner.ref_school = school
                                    accommodation_owner.save()
                                    if accommodation_owner.capacity:
                                        capacity_count = int(
                                            accommodation_owner.capacity)

                                        res = []
                                        arr = [
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 1",
                                                                       price="0.0", code=1, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 2",
                                                                       price="0.0", code=2, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 3",
                                                                       price="0.0", code=3, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 4",
                                                                       price="0.0", code=4, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 5",
                                                                       price="0.0", code=5, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 6",
                                                                       price="0.0", code=6, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 7",
                                                                       price="0.0", code=7, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 8",
                                                                       price="0.0", code=8, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 9",
                                                                       price="0.0", code=9, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 10",
                                                                       price="0.0", code=10, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 11",
                                                                       price="0.0", code=11, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 12",
                                                                       price="0.0", code=12, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 13",
                                                                       price="0.0", code=13, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 14",
                                                                       price="0.0", code=14, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 15",
                                                                       price="0.0", code=15, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 16",
                                                                       price="0.0", code=16, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 17",
                                                                       price="0.0", code=17, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 18",
                                                                       price="0.0", code=18, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 19",
                                                                       price="0.0", code=19, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 20",
                                                                       price="0.0", code=20, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 21",
                                                                       price="0.0", code=21, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 22",
                                                                       price="0.0", code=22, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 23",
                                                                       price="0.0", code=23, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 24",
                                                                       price="0.0", code=25, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 25",
                                                                       price="0.0", code=25, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 26",
                                                                       price="0.0", code=26, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 27",
                                                                       price="0.0", code=27, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 28",
                                                                       price="0.0", code=28, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 29",
                                                                       price="0.0", code=29, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 30",
                                                                       price="0.0", code=30, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 31",
                                                                       price="0.0", code=31, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 32",
                                                                       price="0.0", code=32, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 33",
                                                                       price="0.0", code=33, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 34",
                                                                       price="0.0", code=34, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 35",
                                                                       price="0.0", code=35, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 36",
                                                                       price="0.0", code=36, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 37",
                                                                       price="0.0", code=37, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 38",
                                                                       price="0.0", code=38, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 39",
                                                                       price="0.0", code=39, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 40",
                                                                       price="0.0", code=40, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 41",
                                                                       price="0.0", code=41, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 42",
                                                                       price="0.0", code=42, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 43",
                                                                       price="0.0", code=43, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 44",
                                                                       price="0.0", code=44, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 45",
                                                                       price="0.0", code=45, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 46",
                                                                       price="0.0", code=46, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 47",
                                                                       price="0.0", code=47, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 48",
                                                                       price="0.0", code=48, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 49",
                                                                       price="0.0", code=49, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 50",
                                                                       price="0.0", code=50, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 51",
                                                                       price="0.0", code=51, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 52",
                                                                       price="0.0", code=52, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 53",
                                                                       price="0.0", code=53, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 54",
                                                                       price="0.0", code=54, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 55",
                                                                       price="0.0", code=55, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 56",
                                                                       price="0.0", code=56, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 57",
                                                                       price="0.0", code=57, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 58",
                                                                       price="0.0", code=58, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 59",
                                                                       price="0.0", code=59, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 60",
                                                                       price="0.0", code=60, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 61",
                                                                       price="0.0", code=61, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 62",
                                                                       price="0.0", code=62, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 63",
                                                                       price="0.0", code=63, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 64",
                                                                       price="0.0", code=64, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 65",
                                                                       price="0.0", code=65, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 66",
                                                                       price="0.0", code=66, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 67",
                                                                       price="0.0", code=67, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 68",
                                                                       price="0.0", code=68, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 69",
                                                                       price="0.0", code=69, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 70",
                                                                       price="0.0", code=70, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 71",
                                                                       price="0.0", code=71, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 72",
                                                                       price="0.0", code=72, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 73",
                                                                       price="0.0", code=73, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 74",
                                                                       price="0.0", code=74, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 75",
                                                                       price="0.0", code=75, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 76",
                                                                       price="0.0", code=76, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 77",
                                                                       price="0.0", code=77, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 78",
                                                                       price="0.0", code=78, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 79",
                                                                       price="0.0", code=79, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 80",
                                                                       price="0.0", code=80, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 81",
                                                                       price="0.0", code=81, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 82",
                                                                       price="0.0", code=82, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 83",
                                                                       price="0.0", code=83, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 84",
                                                                       price="0.0", code=84, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 85",
                                                                       price="0.0", code=85, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 86",
                                                                       price="0.0", code=86, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 87",
                                                                       price="0.0", code=87, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 88",
                                                                       price="0.0", code=88, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 89",
                                                                       price="0.0", code=89, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 90",
                                                                       price="0.0", code=90, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 91",
                                                                       price="0.0", code=91, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 92",
                                                                       price="0.0", code=92, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 93",
                                                                       price="0.0", code=93, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 94",
                                                                       price="0.0", code=94, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 95",
                                                                       price="0.0", code=95, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 96",
                                                                       price="0.0", code=96, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 97",
                                                                       price="0.0", code=97, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 98",
                                                                       price="0.0", code=98, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 99",
                                                                       price="0.0", code=99, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 100",
                                                                       price="0.0", code=100, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                        ]
                                        for item in arr:
                                            if (item.code <= capacity_count):
                                                res.append(item)
                                                print(res)
                                        try:
                                            SchoolAccommodationService.objects.bulk_create(
                                                res)
                                        except:
                                            print(
                                                "==================SchoolAccommodationService Not craete")
                                    else:
                                        pass
                                    return redirect('web:create_school_accommodation_owner_next_page_room', pk=accommodation_owner.id)
                                else:
                                    print("Form is not valid")
                                    error = "Capacity will be highest no 100"
                                    form.add_error(None, error)
                            else:
                                error = "Hotel/Hotsel name required!"
                                form.add_error(None, error)
                        else:
                            error = "Please select type"
                            form.add_error(None, error)

                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)

                context['school'] = school
                context['form'] = form
                return render(request, 'admin/master/accommodationowner/create_school_accommodation_owner.html', context)
            else:
                raise_permission_denied = True
        except School.DoesNotExist:
            raise_permission_denied = True

    elif request.user.is_superuser:
        try:
            school = School.objects.get(id=pk)
            if school.id:
                school = School.objects.filter(pk=pk)
                school = school.first()
                context = {}
                form = SchoolAccommodationOwnerForm(request.POST or None)
                data = request.POST.dict()
                if request.method == 'POST':
                    if form.is_valid():
                        accommodation_owner = form.save(commit=False)
                        type_id = accommodation_owner.accommodation_type
                        # print(type(type_id))
                        if accommodation_owner.accommodation_type == 0:
                            if accommodation_owner.first_name and accommodation_owner.last_name:
                                capacity_value = 11
                                capacity_input_value = int(
                                    accommodation_owner.capacity)
                                if (capacity_value > capacity_input_value):
                                    accommodation_owner.ref_school = school
                                    accommodation_owner.save()
                                    if accommodation_owner.capacity:
                                        capacity_count = int(
                                            accommodation_owner.capacity)

                                        res = []
                                        arr = [
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 1",
                                                                       price="0.0", code=1, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 2",
                                                                       price="0.0", code=2, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 3",
                                                                       price="0.0", code=3, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 4",
                                                                       price="0.0", code=4, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 5",
                                                                       price="0.0", code=5, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 6",
                                                                       price="0.0", code=6, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 7",
                                                                       price="0.0", code=7, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 8",
                                                                       price="0.0", code=8, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 9",
                                                                       price="0.0", code=9, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 10",
                                                                       price="0.0", code=10, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1)
                                        ]
                                        for item in arr:
                                            if (item.code <= capacity_count):
                                                res.append(item)
                                                print(res)
                                        try:
                                            SchoolAccommodationService.objects.bulk_create(
                                                res)
                                        except:
                                            print(
                                                "==================SchoolAccommodationService Not craete")
                                    else:
                                        pass
                                    return redirect('web:create_school_accommodation_owner_next_page_room', pk=accommodation_owner.id)
                                else:
                                    print("Form is not valid")
                                    error = "Capacity will be highest no 10"
                                    form.add_error(None, error)
                            else:
                                error = "First name and last is required!"
                                form.add_error(None, error)

                        elif accommodation_owner.accommodation_type == 1:
                            if accommodation_owner.company_name:
                                capacity_value = 101
                                capacity_input_value = int(
                                    accommodation_owner.capacity)
                                if (capacity_value > capacity_input_value):
                                    accommodation_owner.ref_school = school
                                    accommodation_owner.save()
                                    if accommodation_owner.capacity:
                                        capacity_count = int(
                                            accommodation_owner.capacity)

                                        res = []
                                        arr = [
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 1",
                                                                       price="0.0", code=1, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 2",
                                                                       price="0.0", code=2, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 3",
                                                                       price="0.0", code=3, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 4",
                                                                       price="0.0", code=4, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 5",
                                                                       price="0.0", code=5, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 6",
                                                                       price="0.0", code=6, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 7",
                                                                       price="0.0", code=7, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 8",
                                                                       price="0.0", code=8, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 9",
                                                                       price="0.0", code=9, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 10",
                                                                       price="0.0", code=10, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 11",
                                                                       price="0.0", code=11, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 12",
                                                                       price="0.0", code=12, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 13",
                                                                       price="0.0", code=13, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 14",
                                                                       price="0.0", code=14, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 15",
                                                                       price="0.0", code=15, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 16",
                                                                       price="0.0", code=16, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 17",
                                                                       price="0.0", code=17, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 18",
                                                                       price="0.0", code=18, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 19",
                                                                       price="0.0", code=19, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 20",
                                                                       price="0.0", code=20, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 21",
                                                                       price="0.0", code=21, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 22",
                                                                       price="0.0", code=22, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 23",
                                                                       price="0.0", code=23, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 24",
                                                                       price="0.0", code=25, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 25",
                                                                       price="0.0", code=25, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 26",
                                                                       price="0.0", code=26, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 27",
                                                                       price="0.0", code=27, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 28",
                                                                       price="0.0", code=28, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 29",
                                                                       price="0.0", code=29, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 30",
                                                                       price="0.0", code=30, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 31",
                                                                       price="0.0", code=31, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 32",
                                                                       price="0.0", code=32, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 33",
                                                                       price="0.0", code=33, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 34",
                                                                       price="0.0", code=34, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 35",
                                                                       price="0.0", code=35, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 36",
                                                                       price="0.0", code=36, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 37",
                                                                       price="0.0", code=37, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 38",
                                                                       price="0.0", code=38, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 39",
                                                                       price="0.0", code=39, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 40",
                                                                       price="0.0", code=40, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 41",
                                                                       price="0.0", code=41, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 42",
                                                                       price="0.0", code=42, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 43",
                                                                       price="0.0", code=43, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 44",
                                                                       price="0.0", code=44, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 45",
                                                                       price="0.0", code=45, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 46",
                                                                       price="0.0", code=46, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 47",
                                                                       price="0.0", code=47, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 48",
                                                                       price="0.0", code=48, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 49",
                                                                       price="0.0", code=49, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 50",
                                                                       price="0.0", code=50, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 51",
                                                                       price="0.0", code=51, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 52",
                                                                       price="0.0", code=52, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 53",
                                                                       price="0.0", code=53, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 54",
                                                                       price="0.0", code=54, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 55",
                                                                       price="0.0", code=55, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 56",
                                                                       price="0.0", code=56, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 57",
                                                                       price="0.0", code=57, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 58",
                                                                       price="0.0", code=58, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 59",
                                                                       price="0.0", code=59, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 60",
                                                                       price="0.0", code=60, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 61",
                                                                       price="0.0", code=61, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 62",
                                                                       price="0.0", code=62, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 63",
                                                                       price="0.0", code=63, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 64",
                                                                       price="0.0", code=64, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 65",
                                                                       price="0.0", code=65, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 66",
                                                                       price="0.0", code=66, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 67",
                                                                       price="0.0", code=67, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 68",
                                                                       price="0.0", code=68, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 69",
                                                                       price="0.0", code=69, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 70",
                                                                       price="0.0", code=70, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 71",
                                                                       price="0.0", code=71, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 72",
                                                                       price="0.0", code=72, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 73",
                                                                       price="0.0", code=73, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 74",
                                                                       price="0.0", code=74, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 75",
                                                                       price="0.0", code=75, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 76",
                                                                       price="0.0", code=76, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 77",
                                                                       price="0.0", code=77, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 78",
                                                                       price="0.0", code=78, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 79",
                                                                       price="0.0", code=79, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 80",
                                                                       price="0.0", code=80, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 81",
                                                                       price="0.0", code=81, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 82",
                                                                       price="0.0", code=82, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 83",
                                                                       price="0.0", code=83, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 84",
                                                                       price="0.0", code=84, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 85",
                                                                       price="0.0", code=85, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 86",
                                                                       price="0.0", code=86, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 87",
                                                                       price="0.0", code=87, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 88",
                                                                       price="0.0", code=88, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 89",
                                                                       price="0.0", code=89, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 90",
                                                                       price="0.0", code=90, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 91",
                                                                       price="0.0", code=91, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 92",
                                                                       price="0.0", code=92, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 93",
                                                                       price="0.0", code=93, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 94",
                                                                       price="0.0", code=94, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 95",
                                                                       price="0.0", code=95, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 96",
                                                                       price="0.0", code=96, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 97",
                                                                       price="0.0", code=97, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 98",
                                                                       price="0.0", code=98, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 99",
                                                                       price="0.0", code=99, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 100",
                                                                       price="0.0", code=100, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                        ]
                                        for item in arr:
                                            if (item.code <= capacity_count):
                                                res.append(item)
                                                print(res)
                                        try:
                                            SchoolAccommodationService.objects.bulk_create(
                                                res)
                                        except:
                                            print(
                                                "==================SchoolAccommodationService Not craete")
                                    else:
                                        pass
                                    return redirect('web:create_school_accommodation_owner_next_page_room', pk=accommodation_owner.id)
                                else:
                                    print("Form is not valid")
                                    error = "Capacity will be highest no 100"
                                    form.add_error(None, error)
                            else:
                                error = "Resident name required!"
                                form.add_error(None, error)
                        elif accommodation_owner.accommodation_type == 2:
                            if accommodation_owner.company_name:
                                capacity_value = 101
                                capacity_input_value = int(
                                    accommodation_owner.capacity)
                                if (capacity_value > capacity_input_value):
                                    accommodation_owner.ref_school = school
                                    accommodation_owner.save()
                                    if accommodation_owner.capacity:
                                        capacity_count = int(
                                            accommodation_owner.capacity)

                                        res = []
                                        arr = [
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 1",
                                                                       price="0.0", code=1, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 2",
                                                                       price="0.0", code=2, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 3",
                                                                       price="0.0", code=3, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 4",
                                                                       price="0.0", code=4, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 5",
                                                                       price="0.0", code=5, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 6",
                                                                       price="0.0", code=6, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 7",
                                                                       price="0.0", code=7, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 8",
                                                                       price="0.0", code=8, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 9",
                                                                       price="0.0", code=9, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 10",
                                                                       price="0.0", code=10, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 11",
                                                                       price="0.0", code=11, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 12",
                                                                       price="0.0", code=12, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 13",
                                                                       price="0.0", code=13, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 14",
                                                                       price="0.0", code=14, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 15",
                                                                       price="0.0", code=15, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 16",
                                                                       price="0.0", code=16, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 17",
                                                                       price="0.0", code=17, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 18",
                                                                       price="0.0", code=18, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 19",
                                                                       price="0.0", code=19, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 20",
                                                                       price="0.0", code=20, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 21",
                                                                       price="0.0", code=21, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 22",
                                                                       price="0.0", code=22, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 23",
                                                                       price="0.0", code=23, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 24",
                                                                       price="0.0", code=25, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 25",
                                                                       price="0.0", code=25, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 26",
                                                                       price="0.0", code=26, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 27",
                                                                       price="0.0", code=27, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 28",
                                                                       price="0.0", code=28, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 29",
                                                                       price="0.0", code=29, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 30",
                                                                       price="0.0", code=30, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 31",
                                                                       price="0.0", code=31, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 32",
                                                                       price="0.0", code=32, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 33",
                                                                       price="0.0", code=33, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 34",
                                                                       price="0.0", code=34, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 35",
                                                                       price="0.0", code=35, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 36",
                                                                       price="0.0", code=36, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 37",
                                                                       price="0.0", code=37, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 38",
                                                                       price="0.0", code=38, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 39",
                                                                       price="0.0", code=39, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 40",
                                                                       price="0.0", code=40, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 41",
                                                                       price="0.0", code=41, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 42",
                                                                       price="0.0", code=42, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 43",
                                                                       price="0.0", code=43, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 44",
                                                                       price="0.0", code=44, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 45",
                                                                       price="0.0", code=45, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 46",
                                                                       price="0.0", code=46, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 47",
                                                                       price="0.0", code=47, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 48",
                                                                       price="0.0", code=48, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 49",
                                                                       price="0.0", code=49, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 50",
                                                                       price="0.0", code=50, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 51",
                                                                       price="0.0", code=51, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 52",
                                                                       price="0.0", code=52, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 53",
                                                                       price="0.0", code=53, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 54",
                                                                       price="0.0", code=54, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 55",
                                                                       price="0.0", code=55, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 56",
                                                                       price="0.0", code=56, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 57",
                                                                       price="0.0", code=57, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 58",
                                                                       price="0.0", code=58, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 59",
                                                                       price="0.0", code=59, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 60",
                                                                       price="0.0", code=60, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 61",
                                                                       price="0.0", code=61, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 62",
                                                                       price="0.0", code=62, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 63",
                                                                       price="0.0", code=63, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 64",
                                                                       price="0.0", code=64, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 65",
                                                                       price="0.0", code=65, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 66",
                                                                       price="0.0", code=66, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 67",
                                                                       price="0.0", code=67, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 68",
                                                                       price="0.0", code=68, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 69",
                                                                       price="0.0", code=69, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 70",
                                                                       price="0.0", code=70, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 71",
                                                                       price="0.0", code=71, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 72",
                                                                       price="0.0", code=72, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 73",
                                                                       price="0.0", code=73, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 74",
                                                                       price="0.0", code=74, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 75",
                                                                       price="0.0", code=75, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 76",
                                                                       price="0.0", code=76, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 77",
                                                                       price="0.0", code=77, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 78",
                                                                       price="0.0", code=78, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 79",
                                                                       price="0.0", code=79, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 80",
                                                                       price="0.0", code=80, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 81",
                                                                       price="0.0", code=81, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 82",
                                                                       price="0.0", code=82, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 83",
                                                                       price="0.0", code=83, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 84",
                                                                       price="0.0", code=84, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 85",
                                                                       price="0.0", code=85, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 86",
                                                                       price="0.0", code=86, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 87",
                                                                       price="0.0", code=87, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 88",
                                                                       price="0.0", code=88, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 89",
                                                                       price="0.0", code=89, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 90",
                                                                       price="0.0", code=90, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 91",
                                                                       price="0.0", code=91, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 92",
                                                                       price="0.0", code=92, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 93",
                                                                       price="0.0", code=93, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 94",
                                                                       price="0.0", code=94, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 95",
                                                                       price="0.0", code=95, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 96",
                                                                       price="0.0", code=96, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 97",
                                                                       price="0.0", code=97, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 98",
                                                                       price="0.0", code=98, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 99",
                                                                       price="0.0", code=99, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                            SchoolAccommodationService(ref_school_id=accommodation_owner.ref_school.id, accommodation_title="Title 100",
                                                                       price="0.0", code=100, ref_accommodation_owner_id=accommodation_owner.id, status=False, created_by_id=1),
                                        ]
                                        for item in arr:
                                            if (item.code <= capacity_count):
                                                res.append(item)
                                                print(res)
                                        try:
                                            SchoolAccommodationService.objects.bulk_create(
                                                res)
                                        except:
                                            print(
                                                "==================SchoolAccommodationService Not craete")
                                    else:
                                        pass
                                    return redirect('web:create_school_accommodation_owner_next_page_room', pk=accommodation_owner.id)
                                else:
                                    print("Form is not valid")
                                    error = "Capacity will be highest no 100"
                                    form.add_error(None, error)
                            else:
                                error = "Hotel/Hotsel name required!"
                                form.add_error(None, error)
                        else:
                            error = "Please select type"
                            form.add_error(None, error)

                    else:
                        print("Form is not valid")
                        error = "Form is not valid"
                        form.add_error(None, error)

                context['school'] = school
                context['form'] = form
                return render(request, 'admin/master/accommodationowner/create_school_accommodation_owner.html', context)
            else:
                raise_permission_denied = True
        except School.DoesNotExist:
            raise_permission_denied = True

    else:
        raise_permission_denied = True

    if raise_permission_denied:
        raise PermissionDenied()


class DetailSchoolAccommodationOwner(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ('db.view_schoolaccommodationowner',)
    model = SchoolAccommodationOwner
    context_object_name = 'accommodationowner'
    template_name = 'admin/master/accommodationowner/accommodation_owner_detail.html'

    def get_user(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        user = self.get_user()
        raise_permission_denied = False

        if user.groups.filter(name='school').exists():
            logged_in_user = user.organizationuserprofile.ref_school.id
            owner_id = self.kwargs.get('pk', None)
            owner = SchoolAccommodationOwner.objects.get(id=owner_id)
            if logged_in_user == owner.ref_school.id:
                context = super(DetailSchoolAccommodationOwner,
                                self).get_context_data(**kwargs)
                context['accommodation_service'] = SchoolAccommodationService.objects.filter(
                    ref_accommodation_owner=owner_id).order_by("id")
                context['bank_detail'] = SchoolAccommodationAccBank.objects.filter(
                    ref_accommodation=owner_id).order_by("id")
                return context
            else:
                raise_permission_denied = True

        elif user.groups.filter(name='organization').exists():
            logged_in_user = user.organizationuserprofile.ref_organization.id
            owner_id = self.kwargs.get('pk', None)
            owner = SchoolAccommodationOwner.objects.get(id=owner_id)

            if logged_in_user == owner.ref_school.ref_organization.id:
                context = super(DetailSchoolAccommodationOwner,
                                self).get_context_data(**kwargs)
                context['accommodation_service'] = SchoolAccommodationService.objects.filter(
                    ref_accommodation_owner=owner_id).order_by("id")
                return context
            else:
                raise_permission_denied = True

        elif user.groups.filter(name='admin').exists():
            if logged_in_user == owner.ref_school.id:
                context = super(DetailSchoolAccommodationOwner,
                                self).get_context_data(**kwargs)
                context['accommodation_service'] = SchoolAccommodationService.objects.filter(
                    ref_accommodation_owner=owner_id).order_by("id")
                return context
            else:
                raise_permission_denied = True

        elif user.is_superuser:
            school_id = self.kwargs.get('pk', None)
            context = super(DetailSchoolAccommodationOwner,
                            self).get_context_data(**kwargs)
            logged_in_user = user.is_superuser
            owner_id = self.kwargs.get('pk', None)
            owner = SchoolAccommodationOwner.objects.get(id=owner_id)
            if logged_in_user:
                context['accommodation_service'] = SchoolAccommodationService.objects.filter(
                    ref_accommodation_owner=owner_id).order_by("id")
                context['bank_detail'] = SchoolAccommodationAccBank.objects.filter(
                    ref_accommodation=owner_id).order_by("id")
                return context
            else:
                raise_permission_denied = True

        else:
            raise_permission_denied = True

        if raise_permission_denied:
            raise PermissionDenied()


@login_required
@permission_required(['db.delete_schoolaccommodationowner'], raise_exception=True)
def delete_school_accommodation_owner(request, pk):
    user = request.user
    raise_permission_denied = False

    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        print(logged_in_user)
        try:
            owner = SchoolAccommodationOwner.objects.get(id=pk)
            _id = owner.ref_school.id

            if logged_in_user == _id:
                if request.method == 'POST':
                    owner.delete()
                    print("Delete Successfully")
                    return redirect('web:deatil_school', pk=owner.ref_school.id)
                else:
                    pass
                return render(request, 'admin/master/accommodationowner/delete_school_accommodation_owner.html', {'owner': owner, 'school': owner.ref_school.id})
            else:
                print("==============================auth error===========")
                raise_permission_denied = True

        except:
            print("==============================try error===========")
            raise_permission_denied = True

    elif user.groups.filter(name='admin').exists() or user.is_superuser:
        try:
            owner = SchoolAccommodationOwner.objects.get(id=pk)
            _id = owner.ref_school.id

            if _id:
                if request.method == 'POST':
                    owner.delete()
                    print("Delete Successfully")
                    return redirect('web:deatil_school', pk=owner.ref_school.id)
                else:
                    pass
                return render(request, 'admin/master/accommodationowner/delete_school_accommodation_owner.html', {'owner': owner, 'school': owner.ref_school.id})
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
@permission_required(['db.add_schoolaccommodationservice'], raise_exception=True)
def create_school_accommodation_owner_next_page_room(request, pk):
    user = request.user
    if user.groups.filter(name='school').exists():
        logged_in_user = request.user.organizationuserprofile.ref_school.id
        try:
            owner_id = SchoolAccommodationOwner.objects.get(id=pk)
            if logged_in_user == owner_id.ref_school.id:
                context = {}
                SchoolAccommodationServiceFormset = modelformset_factory(
                    SchoolAccommodationService, form=SchoolAccommodationServiceForm,  extra=0)
                qs = SchoolAccommodationService.objects.filter(
                    ref_accommodation_owner=owner_id)
                formset = SchoolAccommodationServiceFormset(
                    request.POST or None, queryset=qs)
                if request.method == "POST":
                    print("==================================Post============")
                    if formset.is_valid():
                        # print(formset)
                        for data in formset:
                            print("===============forloop=========")
                            print(data)
                            data.save()
                        return redirect('web:detail_school_accommodation_owner', pk=owner_id)

                    else:
                        print(formset.errors)
                        print("=================Form Not valid===============")

                context['owner_id'] = owner_id
                context['formset'] = formset
                return render(request, 'admin/master/accommodationowner/create_school_accommodation_owner_next_page_room.html', context)
            else:
                permission = "permission"
                return render(request, 'admin/master/accommodationowner/create_school_accommodation_owner_next_page_room.html', {'permission': permission})

        except SchoolAccommodationOwner.DoesNotExist:
            permission = "permission"
            return render(request, 'admin/master/accommodationowner/create_school_accommodation_owner_next_page_room.html', {'permission': permission})

    elif request.user.is_superuser:

        try:
            owner_id = SchoolAccommodationOwner.objects.get(id=pk)
            if owner_id.ref_school.id:
                context = {}
                SchoolAccommodationServiceFormset = modelformset_factory(
                    SchoolAccommodationService, form=SchoolAccommodationServiceForm,  extra=0)
                qs = SchoolAccommodationService.objects.filter(
                    ref_accommodation_owner=owner_id)
                formset = SchoolAccommodationServiceFormset(
                    request.POST or None, queryset=qs)
                if request.method == "POST":
                    print("==================================Post============")
                    if formset.is_valid():
                        # print(formset)
                        for data in formset:
                            print("===============forloop=========")
                            print(data)
                            data.save()
                        return redirect('web:detail_school_accommodation_owner', pk=owner_id)

                    else:
                        print(formset.errors)
                        print("=================Form Not valid===============")

                context['owner_id'] = owner_id
                context['formset'] = formset
                return render(request, 'admin/master/accommodationowner/create_school_accommodation_owner_next_page_room.html', context)
            else:
                permission = "permission"
                return render(request, 'admin/master/accommodationowner/create_school_accommodation_owner_next_page_room.html', {'permission': permission})

        except SchoolAccommodationOwner.DoesNotExist:
            permission = "permission"
            return render(request, 'admin/master/accommodationowner/create_school_accommodation_owner_next_page_room.html', {'permission': permission})

    else:
        permission = "permission"
        return render(request, 'admin/master/accommodationowner/create_school_accommodation_owner_next_page_room.html', {'permission': permission})

