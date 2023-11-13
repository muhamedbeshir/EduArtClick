from django.db import models

from v1.base.models.model import BaseModel, BaseModelMeta
from v1.db.master.school import School


class SchoolSponsor(BaseModel, models.Model):
    ref_school = models.ForeignKey(
        School, related_name="rel_ref_school_school_sponsor", on_delete=models.CASCADE)
    name = models.CharField(max_length=255,)
    email = models.EmailField(max_length=255,)
    address = models.TextField(max_length=500,)

    Meta = BaseModelMeta(
        attr={
            "db_table": "school_sponsor",
            "unique_together": ("ref_school", "email",)
        },
        app_name='db'
    )

    def __str__(self) -> str:
        return str(self.name).title()
