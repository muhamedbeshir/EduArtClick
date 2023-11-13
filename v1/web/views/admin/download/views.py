from django.conf import settings
from django.shortcuts import render,redirect
from django.views.generic import  View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage, send_mail

from django.template.loader import render_to_string
from v1.base.utils.pdf import PDFRender
from django.template.loader import get_template

import datetime

from datetime import date, timedelta

from v1.db.models import *



class DownloadCertificatePDF(View):
	def get(self, request, *args, **kwargs):
		html = get_template('admin/download/certificate_pdf.html')
		_pk = kwargs['pk']
		_model = SchoolCertificate.objects.filter(
                id=_pk)
		if _model.exists():
			certificate =_model.get()
			title = "Certificate"
			ctx = {
				'title': title,
				'certificate':certificate
			}
			html = html.render(ctx)
			options = {
				'page-size': 'A4',
			}
			
			no = certificate.id #certificate.ref_cert.ref_course
			file='certificate'+'.pdf'
			#return Response(ctx)
			return PDFRender.render(html, file_name=file, **options)


			
