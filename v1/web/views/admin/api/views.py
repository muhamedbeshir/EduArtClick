import json
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View
from django.core.serializers import serialize

from v1.db.models import *

class CourseDetailAjax(View):
    def get(self, request, *args, **kwargs):
    	course_id = request.GET.get('course')
    	data = json.dumps({
    		"service": "service",
    		"price": "price"
    	})
    	return HttpResponse(data, content_type='application/json')

def course_detail_ajax(request):
	course_id = request.GET.get('course')
	c_id=SchoolCourse.objects.get(pk=course_id)
	print(c_id.ref_school.id)
	services = SchoolService.objects.filter(ref_school=c_id.ref_school.id)
	print(services)

	price_list = SchoolCoursePrice.objects.filter(ref_school_course=course_id).order_by('min_weak')
	
	return render(request, 'admin/api/course_detail_ajax.html', {'price_list':price_list,'services':services})

