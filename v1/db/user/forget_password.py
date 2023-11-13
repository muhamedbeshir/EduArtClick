from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta


class AuthForgetPasswordToken(BaseModel, models.Model):
    user = models.ForeignKey(
        User, related_name="auth_forget_password", on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now_add=True)

    Meta = BaseModelMeta(
        attr={"db_table": "auth_forget_password_token"}, app_name='db')
