from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "自定义管理后台"
    site_title = "自定义管理后台"
    index_title = "欢迎来到自定义管理后台"