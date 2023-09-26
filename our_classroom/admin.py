from django.contrib import admin
from . import models
# Register your models here.


class LecturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'department']


class ProgramAdmin(admin.ModelAdmin):
    list_display = ['program_name', 'department']


class LevelAdmin(admin.ModelAdmin):
    list_display = ['level', 'semester']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'lecturer', 'program_it_belongs_to', 'level']


class InformationCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class InformationAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'message', 'is_active', 'is_done']


class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['program', 'level', 'session', 'activated']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['dept_name', 'head_of_dept']


class AuthCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'used']


admin.site.register(models.Lecturer, LecturerAdmin)
admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.Level, LevelAdmin)
admin.site.register(models.Program, ProgramAdmin)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.InformationCategory, InformationCategoryAdmin)
admin.site.register(models.Information, InformationAdmin)
admin.site.register(models.StudentClass, StudentClassAdmin)
admin.site.register(models.CustomUser)
admin.site.register(models.AuthCode, AuthCodeAdmin)
