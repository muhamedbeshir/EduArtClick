import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

from v1.base.configs import const as CONST

from django.core.mail import send_mail

class cMailer():
    cData = {"template_id": 0}
    fData = {"template_id": "", "vars": []}
    personalization = {"to_list": []}
    response = {}
    errors = {}

    is_mail_sent = False

    def get_db_template_data(self):
        from db.models import MailTemplates
        model = MailTemplates.objects.filter(id=self.cData["template_id"])
        if model.exists():
            self.cData["db_model"] = model.get()
        else:
            self.errors = {"message": "Mail Template Not Found!"}

    def get_db_template(self):
        # Mail Template 1 for the signup password set
        if self.fData["template_id"] == 1:
            self.cData["template_id"] = 1

        # Mail Template 2
        elif self.fData["template_id"] == 2:
            self.cData["template_id"] = 2

        # Mail Template 3 for Cron to notify the user when Sample Expires
        elif self.fData["template_id"] == 3:
            self.cData["template_id"] = 3

        if (self.cData["template_id"] > 0):
            self.get_db_template_data()
        else:
            self.errors = {"message": "Invalid Mail Template ID!"}

    def init(self, **kwargs):
        self.set_vars(**kwargs)

    def set_vars(self, **kwargs):
        """Sets the class Vars."""

        self.cData["from_email"] = Email("qms@nqraa.com", "NQRAA")

        if 'to_list' in kwargs:
            to_list = []
            for _list in kwargs["to_list"]:
                to_list.append( _list.get( "email" ) )
            
            self.fData["to_list"] = to_list

        if 'template_id' in kwargs:
            self.fData["template_id"] = kwargs["template_id"]
            self.get_db_template()

        if 'substitutions' in kwargs:
            self.fData["substitutions"] = kwargs["substitutions"]

    def get_mail_body(self):
        content = self.cData["db_model"].content

        for data in self.fData["substitutions"]:
            key = "{{" + data["key"] + "}}"
            content = content.replace(key, data["value"])

        return content

    def get_mail(self):
        message = self.get_mail_body()

        data = {
            "subject": self.cData["db_model"].subject,
            "message" : message,
            "html_message": message,
            "from_email": self.cData["from_email"].email,
            "recipient_list" : self.fData["to_list"]
        }

        return data  

    def send_mail(self):
        if(self.has_errors() == False):
            data = self.get_mail()
            try:
                res = send_mail(**data)
                self.is_mail_sent = True
            except Exception as e:
                self.errors = { "message" : "Mail not Sent!" , "info" : e.args }

    def save_response(self):
        pass

    def has_errors(self):
        return self.errors.get("message") is not None

