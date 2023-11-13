import re
from django.db import models

from os import path
from PIL import Image
from random import randint

from django.utils import timezone

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta
from django.db import models

from v1.db.master.school_course_level import SchoolCourseLevel

from ..organization import Organization
from ..master.school import School


def get_filename_ext(filename):
    filepath = path.basename(filename)
    name, ext = path.splitext(filepath)
    return name, ext


def upload_name_path(instance, filename):
    folderName = randint(1, 40000000)
    filenam = randint(1, folderName)
    ext = get_filename_ext(filename)[1]
    return f'organization/{folderName}/{filenam}.{ext}'


class UserProfile(BaseModel, models.Model):
    ref_user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    avtar = models.FileField(upload_to='user', blank=True, null=True)

    @property
    def email(self):
        try:
            userobj = User.objects.get(id=self.ref_user.id)
            return userobj.email
        except:
            return ""

    @property
    def type(self):
        try:
            return self.ref_user.groups.values_list('name', flat=True).first()
        except:
            return ""


class StudentUserProfile(BaseModel, models.Model):
    ref_user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    avtar = models.FileField(upload_to='user', blank=True, null=True)
    terms_and_condition = models.BooleanField(default=False)

    @property
    def email(self):
        try:
            userobj = User.objects.get(id=self.ref_user.id)
            return userobj.email
        except:
            return ""

    @property
    def type(self):
        try:
            return self.ref_user.groups.values_list('name', flat=True).first()
        except:
            return ""


class AggentUserProfile(BaseModel, models.Model):
    ref_user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    avtar = models.FileField(upload_to='user', blank=True, null=True)
    terms_and_condition = models.BooleanField(default=False)

    @property
    def email(self):
        try:
            userobj = User.objects.get(id=self.ref_user.id)
            return userobj.email
        except:
            return ""

    @property
    def type(self):
        try:
            return self.ref_user.groups.values_list('name', flat=True).first()
        except:
            return ""


class OrganizationUserProfile(BaseModel, models.Model):
    ref_user = models.OneToOneField(User, on_delete=models.CASCADE)
    ref_organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="rel_user_profile_ref_organization_organization")
    ref_school = models.ForeignKey(School, on_delete=models.CASCADE,
                                   related_name="rel_user_profile_ref_school_school", blank=True, null=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    avtar = models.FileField(upload_to='user', blank=True, null=True)

    @property
    def email(self):
        try:
            userobj = User.objects.get(id=self.ref_user.id)
            return userobj.email
        except:
            return ""

    @property
    def type(self):
        try:
            return self.ref_user.groups.values_list('name', flat=True).first()
        except:
            return ""


class TeacherUserProfile(BaseModel, models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female')
    )

    ref_user = models.OneToOneField(User, on_delete=models.CASCADE)
    ref_school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="rel_techer_user_profile_ref_school_school")
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    lang_one = models.CharField(max_length=128, blank=True, null=True)
    lang_two = models.CharField(max_length=128, blank=True, null=True)
    lang_three = models.CharField(max_length=128, blank=True, null=True)
    avtar = models.ImageField(upload_to='user', blank=True, null=True)

    @property
    def email(self):
        try:
            userobj = User.objects.get(id=self.ref_user.id)
            return userobj.email
        except:
            return ""

    def __str__(self):
        return self.first_name + " " + self.last_name


class SchoolStudentUserProfile(BaseModel, models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female')
    )

    ref_user = models.OneToOneField(User, on_delete=models.CASCADE)
    ref_school = models.ForeignKey(School, on_delete=models.CASCADE,
                                   related_name="rel_school_student_user_profile_ref_school_school")
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    home_address = models.TextField(blank=True, null=True)
    post_code = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=300)
    phone = models.CharField(max_length=20, blank=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiry_date = models.DateField(blank=True, null=True)
    avtar = models.ImageField(upload_to='user', blank=True, null=True)
    ref_course_level = models.ForeignKey(
        SchoolCourseLevel, related_name="rel_school_student_user_profile_ref_course_level", null=True, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return " ".join([self.first_name, self.last_name])


    @property
    def display_id(self):
        return str(self.ref_user.id)

    @property
    def email(self):
        try:
            userobj = User.objects.get(id=self.ref_user.id)
            return userobj.email
        except:
            return ""
        
    @property
    def username(self):
        return self.ref_user.username

    @property
    def type(self):
        try:
            return self.ref_user.groups.values_list('name', flat=True).first()
        except:
            return ""

    @property
    def gender_title(self):
        res = ""
        for gender in self.GENDER_CHOICES:
            if gender[0] == self.gender:
                res = gender[1]
        return res

    @property
    def name(self):
        return " ".join([self.first_name, self.last_name])
