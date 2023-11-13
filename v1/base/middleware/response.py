from types import MethodType
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
import json , os

import logging
from datetime import datetime

from v1.base.configs import cRequest

class cRepsponseMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        CONTENT_TYPE = request.META.get('CONTENT_TYPE')
        
        if CONTENT_TYPE == "application/json":
            response[ "Content-Type" ] = "application/json; charset=utf-8"
        
        if response.status_code > 300:
            logger = logging.getLogger('cLogs')

            try:
                req = cRequest.request.data
            except:
                req = None

            try:
                user = cRequest.request.user.id
            except:
                user = None

            try:
                res = response.data
            except:
                res = str(response.content[0:256])
            
            obj = { 
                "time" : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")  ,
                "request" : {
                    "method" : request.method ,
                    "url" : request.path,
                    "params" : request.content_params,
                    "body" : req ,
                    "user" : user
                },
                "response" : res
            } 
                
            if response.status_code > 300 and response.status_code < 500:
                logger.warning(json.dumps( obj ))

            elif response.status_code >= 500:
                logger.error(json.dumps(obj))
        
        return response

    # def process_template_response(self, request, response):
    #     if hasattr(response, 'data'):
    #         if response.status_code == 200 or response.status_code == 201:
    #             response.data = {"results": response.data}
    #         elif response.status_code == 204:
    #             pass
    #         else:
    #             response.data = {"errors": response.data}

    #     return response
