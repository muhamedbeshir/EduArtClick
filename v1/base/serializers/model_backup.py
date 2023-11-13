from rest_framework import serializers

from ..models import TrashBackupModel

class TrashBackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrashBackupModel
        fields = '__all__'