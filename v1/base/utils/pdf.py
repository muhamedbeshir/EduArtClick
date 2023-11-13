import os
import pdfkit
from django.http import HttpResponse
from django.template.loader import get_template
#from .template_renderer import TemplateRenderer



class PDFRender:

    @classmethod
    def render(cls, html, file_name, **extra_options):
        options = {
            'page-size': 'A4',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'no-outline': None
        }
        if extra_options:
            options.update(extra_options)

        try:
            pdf = pdfkit.from_string(html, False, options=options)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=' + file_name + ''
        except Exception as e:
            response = HttpResponse("Error Rendering PDF!! Trace: " + str(e), status=400)
        return response
    
    @classmethod
    def generate_pdf_file(cls, html, file_name, **extra_options):

        options = {
            'page-size': 'A4',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'no-outline': None,
            'footer-right': '[page] of [topage]'
        }
        if extra_options:
            options.update(extra_options)

        try:
            pdf = pdfkit.from_string(html, False, options=options)
            return pdf
            # response = HttpResponse(pdf, content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename=' + file_name + ''
        except Exception as e:
            response = HttpResponse("Error Rendering PDF!! Trace: " + str(e), status=400)
        return response

    @classmethod
    def render_from_template(cls, template_path, file_name, context={}):

        options = {
            'page-size': 'A4',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'no-outline': None,
            'footer-right': '[page] of [topage]'
        }

        try:
            html_content = TemplateRenderer.load_template(template_path, context=context)

            kwargs = {}
            wkhtmltopdf_bin = os.environ.get('WKHTMLTOPDF_BIN')
            if wkhtmltopdf_bin:
                kwargs['configuration'] = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_bin)

            pdf = pdfkit.from_string(html_content, False, options=options, **kwargs)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=' + file_name + ''
        except Exception as e:
            response = HttpResponse("Error Rendering PDF!! Trace: " + str(e), status=400)
        return response