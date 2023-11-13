from django.apps import AppConfig

class DbConfig(AppConfig):
    name = "v1.db"
    label = "db"
    table = { "prefix" : "nqraa" }

default_app_config = 'v1.db.DbConfig'