from django.contrib import admin
from .models import Job, Form, AppInfo

# Register your models here.
admin.site.register(Job)
admin.site.register(Form)
admin.site.register(AppInfo)