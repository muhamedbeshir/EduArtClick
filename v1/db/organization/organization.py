from django.db import models

from os import path
# from PIL import Image
from random import randint

from django.utils import timezone

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta


from v1.base.models import BaseModel, BaseModelMeta
from django.db import models
from django.core.validators import URLValidator



def get_filename_ext(filename):
    filepath = path.basename(filename)
    name, ext = path.splitext(filepath)
    return name, ext

def upload_name_path(instance, filename):
    folderName = randint(1, 40000000)
    filenam = randint(1, folderName)
    ext = get_filename_ext(filename)[1]
    return f'organization/{folderName}/{filenam}.{ext}'


class Organization(BaseModel, models.Model):
    organization_name = models.CharField(max_length=200, unique=True)
    organization_logo = models.ImageField(upload_to=upload_name_path, blank=True , null=True)
    web_url = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator, ])

    def __str__(self):
        return '%s' % self.organization_name