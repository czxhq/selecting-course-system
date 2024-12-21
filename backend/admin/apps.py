from django.apps import AppConfig


class AdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    default_site = 'admin.site.CustomAdminSite'
    name = "admin"
