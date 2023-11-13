from django.db import models

from v1.base.models.model import BaseModel, BaseModelMeta
from v1.db.master.school import School
from django.utils.html import format_html


class SchoolSetting(BaseModel, models.Model):   
    ref_school = models.OneToOneField( School , related_name="rel_ref_school_school_setting" , on_delete=models.CASCADE )
    name = models.CharField(max_length=255, verbose_name='Name')
    logo = models.ImageField(upload_to='school/setting', verbose_name='Logo', null=True, blank=True)

    Meta = BaseModelMeta( 
        attr={
            "db_table": "school_setting",
        }, 
        app_name='db'
    )

    def __str__(self) -> str:
        return str(self.name).title()

    def image_tag(self):
        if self.logo:
            return format_html(f'<img src="{self.logo.url}" width="50" height="50" />')
        return 'Not Found'

    def delete(self, using=None, keep_parents=False):
        if self.logo:
            self.logo.storage.delete(self.logo.name)
        return super().delete(using, keep_parents)
        

    image_tag.short_description = 'Image'