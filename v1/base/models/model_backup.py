import json
import datetime

from v1.base import configs

from ..serializers import TrashBackupSerializer, ModelBackupLogSerializer

class cModelBackup():
    __backup_data = {"prev": {}, "curr": {}}

    def custom_json_dumps(self,o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    def _get_user(self):
        try:
            user_id = configs.request.user.id
        except:
            user_id = 0

        return user_id

    def _prepare_data_prev(self):
        setattr(self, '__backup_content_prev', json.dumps({}))
        log_type = self._get_backup_type()

        data = self.__dict__.get( '__backup_content' )

        if(log_type == 2):
            data_prev = self._meta.model.objects.get( id = self.id ).__dict__.copy()
            data_prev.pop( '_state' )

            setattr(self, '__backup_content_prev',  json.dumps(data_prev , default = self.custom_json_dumps ) )      
        elif(log_type == 10):
            setattr(self, '__backup_content_prev', json.dumps(data , default = self.custom_json_dumps ))

    def _prepare_data_curr(self):
        setattr(self, '__backup_data_curr', json.dumps({}))
        log_type = self._get_backup_type()

        data = self.__dict__.get( '__backup_content' )

        if(log_type == 1):
            setattr(self, '__backup_content_curr',  json.dumps(data , default = self.custom_json_dumps))
        elif(log_type == 2):
            setattr(self, '__backup_content_curr',  json.dumps(data , default = self.custom_json_dumps))    
        elif(log_type == 10):
            setattr(self, '__backup_content_curr',  json.dumps({}))

    def _get_backup_type(self):
        return self.__dict__.get('__backup_args').get('type') if 'type' in self.__dict__.get('__backup_args') else 0

    def _prepare_data(self):
        data = self.__dict__.copy()
        data.pop('_state')
        data.pop('__backup_args')

        setattr(self, '__backup_content', data)

        self._prepare_data_prev()
        self._prepare_data_curr()

        model = {
            "app_label": self._meta.app_config.label,
            "model": self._meta.model_name,
            "table_name": self._meta.db_table,
            "log_type": self._get_backup_type(),
            "ref_id": data.get('id'),
            "content_prev": self.__dict__.get('__backup_content_prev'),
            "content_curr": self.__dict__.get('__backup_content_curr'),
            "created_by": self._get_user(),
            "created_at": datetime.datetime.now()
        }

        return model

    def _do_backup(self,  **kwargs):
        setattr(self, '__backup_args', kwargs)

        data = self._prepare_data()
        
        if data[ "content_prev" ] != data[ "content_curr" ] :
            serailizer = ModelBackupLogSerializer(data=data)

            if serailizer.is_valid():
                if serailizer.save():
                    pass
                else:
                    print(serailizer.errors)
            else:
                print(serailizer.errors)
