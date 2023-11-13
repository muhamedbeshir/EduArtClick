from django.db import models
from django.contrib.auth.models import User
from v1.base.models import BaseModel, BaseModelMeta


class Commission(BaseModel, models.Model):

    min_application = models.PositiveSmallIntegerField()
    max_application = models.PositiveSmallIntegerField()
    commission_rate = models.DecimalField(max_digits=4, decimal_places=2)
    is_active = models.BooleanField(default=True, null=True, blank=True, verbose_name='Is Active')

    Meta = BaseModelMeta( attr={
        "db_table": "commission",
        "unique_together": ("min_application", "max_application"),
    }, app_name='db' )

    def __str__(self) -> str:
        return f'[{self.min_application} - {self.max_application}] = {self.commission_rate}%'