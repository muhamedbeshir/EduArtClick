from rest_framework import serializers

from v1.db.models import AuthForgetPasswordToken


class AuthForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthForgetPasswordToken
        #fields = '__all__'
        exclude = ['created_by']


