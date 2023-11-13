from rest_framework import serializers

from ..models import BackupLogModel

class ModelBackupLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupLogModel
        fields = '__all__'