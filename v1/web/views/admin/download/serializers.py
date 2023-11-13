from rest_framework.serializers import Serializer

from v1.base.models import model
from django.db.models import fields
from rest_framework import serializers
from v1.db.models import *




class SchoolCertificateSerializers(serializers.ModelSerializer):
	class Meta:
		model = SchoolCertificate
		fields = ( "id","content")



