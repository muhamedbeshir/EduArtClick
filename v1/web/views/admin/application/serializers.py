from rest_framework import serializers

from v1.db.models import ApplicationToken, ApplicationService


class ApplicationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationToken
        #fields = '__all__'
        exclude = ['created_by']


class ApplicationServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationService
        fields = ('ref_application', 'ap_service_name')
        #exclude = ['created_by']


