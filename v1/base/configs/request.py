from django.conf import settings

class aRequest:
    def __init__(self):
        self.request = dict() 
        self.params = dict()

    def get_image_path_insert(self, url):
        return url.replace(settings.BASE_URL,'')

    def get_image_path(self, url):
        if isinstance(url,str):
            if  "http" ==  url[0:4]:
                return url
            else:
                return settings.BASE_URL + url
        else: 
            return ""        
    
    def get_user_role(self):
        role = None
        
        try:
            user = self.request.user
            print(user)

            if user.is_superuser:
                role = "admin"
            else:    
                roles = user.groups.filter().all()
                for _role in roles:
                    role = _role.name
                    print(role)

        except Exception as e:    
            pass
        
        return role

cRequest = aRequest()
