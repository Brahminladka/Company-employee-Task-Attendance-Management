from django.contrib import admin
from .models import Employee, ProjectMaster, LoginCredential, Attendance

admin.site.register(ProjectMaster)
admin.site.register(LoginCredential)
admin.site.register(Attendance)
admin.site.register(Employee)
