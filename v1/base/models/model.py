from django.apps import apps
from django.db import models
from django.contrib.auth.models import User
from builtins import property, SystemExit, Exception, print, dict, type
from django.db.models.deletion import CASCADE, Collector
from django.db import (
    DEFAULT_DB_ALIAS, DJANGO_VERSION_PICKLE_KEY, DatabaseError, connection,
    connections, router, transaction,
)
from v1.base.configs import cRequest
import json
import datetime

from ..component.error import BaseError

"""
   Base Config Class for the Current App
"""


class CustomBaseConfig():
    attr = {}

    """
        Get the App Config for the Current App
    """
    @classmethod
    def _app_config(cls):
        if cls.app_name is not None:
            try:
                cls.app_config = apps.get_app_config(cls.app_name)
            except:
                ref = {"type": "model", "table_name": ""}

                if cls.__dict__.get('attr') is not None:
                    if cls.__dict__.get('attr').get('db_table') is not None:
                        ref["table_name"] = cls.__dict__.get(
                            'attr').get('db_table')

                BaseError.unmet_dependency(
                    message="App with provided app name is not found!",
                    details={"app_name":  cls.app_name, "ref": ref}
                )
        else:
            ref = {"type": "model", "table_name": ""}
            if cls.__dict__.get('attr') is not None:
                if cls.__dict__.get('attr').get('db_table') is not None:
                    ref["table_name"] = cls.__dict__.get(
                        'attr').get('db_table')

                    BaseError.unmet_dependency(
                        message="app name is not provided in the model Mata Class!",
                        details={"app_name":  cls.app_config.name, "ref": ref}
                    )

            BaseError.unmet_dependency(
                message="table prefix is not defined in the app config!",
                details={"app_name":  cls.app_config.name, "ref": ref}
            )

    """
        Set the necessory class vars for the current class
    """
    @classmethod
    def _cls_app_vars(cls):
        try:
            cls._table = dict({"prefix": cls.app_config.table["prefix"]})
        except Exception as e:
            BaseError.unmet_dependency(
                message="table prefix is not defined in the app config!",
                details={"app_name":  cls.app_config.name},
                error=e
            )

    """
        Init the current config class
    """
    @classmethod
    def init(cls):
        cls._app_config()
        cls._cls_app_vars()

    """
        Set the table name for the model with prefix provided by the app config
    """
    @classmethod
    def _set_table_name(cls, name):
        try:
            cls.attr["db_table"] = cls._table["prefix"] + "_" + name
        except Exception as e:
            BaseError.unmet_dependency(
                message="init method for the class has not been called!",
                details={"class": {"name": "CustomBaseConfig"}},
                error=e,
                extra={"cls": cls}
            )

    """
        Get the table name for the model
    """
    @classmethod
    def _get_table_name(cls):
        try:
            return cls.attr["db_table"]
        except Exception as e:
            BaseError.unmet_dependency(
                message="_set_table_name method for the class has not been called!",
                details={"class":  {"name": "CustomBaseConfig", }},
                error=e,
                extra={"cls": cls}
            )


"""
   Base Meta Class for all the models
"""


class BaseModelMeta(CustomBaseConfig):
    @classmethod
    def __new__(cls, *args, **kwargs):
        cls._set_class_vars(kwargs)

        return type("Meta", cls.bases, cls.attr)

    @classmethod
    def _set_class_vars(cls, kwargs):
        cls.kwargs = kwargs
        cls._set_class_bases()
        cls._set_app_name()
        cls._set_attr()

    @classmethod
    def _set_class_bases(cls):
        cls.bases = cls.kwargs["bases"] if 'bases' in cls.kwargs else ()

    @classmethod
    def _set_app_name(cls):
        cls.app_name = cls.kwargs["app_name"] if 'app_name' in cls.kwargs else None

    @classmethod
    def _set_attr(cls):
        cls.attr = cls.kwargs["attr"] if 'attr' in cls.kwargs else {}
        cls._set_attr_table_name()

    @classmethod
    def _set_attr_table_name(cls):
        if 'db_table' in cls.attr:
            cls.init()
            cls._set_table_name(cls.attr["db_table"])
        else:
            BaseError.unmet_dependency(
                message="attr db_table is not set for the model!",
                details={"class": {"name": "ModelBaseMeta"}},
                extra={'cls': cls}
            )


class BaseModel(models.Model):
    created_by = models.ForeignKey(User, related_name="created_by_%(class)s", on_delete=models.CASCADE,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)


    class Meta:
        abstract = True

    def day_suffix(self,day):
        suffix = ""
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        return suffix

    def date_formatter(self,date,format):
        try:
            if format == "-dsMMMYYYY":
                return date.strftime( "%-d" + self.day_suffix( date.day ) + " %B %Y" )
            elif format == "dsMMMYYYY":
                return date.strftime( "%d" + self.day_suffix( date.day ) + " %B %Y" )
            elif format == "dMMMYYYY":
                return date.strftime( "%d" + " %B %Y" )
            elif format == "dmmmYYYY":
                return date.strftime( "%d" + " %b %Y" )
            elif format == "HHIIA":
                return date.strftime( "%I:%M %p" )
            elif format == "ymd":
                return date.strftime( "%Y-%m-%d" )   
        except:
            return "" 

        return ""    

    def delete(self, using=None, keep_parents=False):
        #self._do_backup(type=10)
        return models.Model.delete(self, using=None, keep_parents=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        model = {}
        try:
            self.created_by = self.request.user
            print(self.created_by)
        except:
            self.created_by_id = 1

        if self.__dict__.get( 'id' ) is None:
            model = models.Model.save(self, force_insert=False, force_update=False, using=None,
                                      update_fields=None)
            #self._do_backup(type=1)
        else:
            #self._do_backup(type=2)
            model = models.Model.save(self, force_insert=False, force_update=False, using=None,
                                  update_fields=None)

        return model
