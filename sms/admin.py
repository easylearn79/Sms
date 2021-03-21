from django.contrib import admin
from .models import Student,Staff,Session,Subject
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
# Register your models here.

class UserModel(UserAdmin):
    ordering = ('email',)

admin.site.register(CustomUser, UserModel)

admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Staff)
