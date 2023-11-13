from rest_framework.authentication import TokenAuthentication

class cTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'