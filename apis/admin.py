from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Term, Professor, Subject, UserData

class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'start_date', 'end_date')

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_id', 'phone_no')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'prof_name', 'term', 'credits')

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

class UserDataInline(admin.StackedInline):
    model = UserData
    can_delete = False
    verbose_name_plural = 'user data'

# class CustomUserAdmin(UserAdmin):
#     inlines = (UserDataInline, )

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)

admin.site.register(Term, TermAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(UserData, UserDataAdmin)


# admin.site.register(User)
# admin.site.register(Term)
# admin.site.register(Professor)
# admin.site.register(Subject)
# admin.site.register(UserData)
