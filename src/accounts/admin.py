from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import Admin, Student, Teacher, User
from accounts.models.student_models import StudentMore


class UserModelAdmin(BaseUserAdmin):
    list_display = ("id", "email", "name", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email", "id")
    filter_horizontal = ()


class AdminModelAdmin(BaseUserAdmin):
    list_display = ("id", "email", "name")
    list_filter = ("is_admin",)
    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email", "id")
    filter_horizontal = ()


class TeacherModelAdmin(BaseUserAdmin):
    list_display = ("id", "email", "name")
    list_filter = ("is_admin",)
    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email", "id")
    filter_horizontal = ()


class StudentMoreTabularInline(admin.StackedInline):
    model = StudentMore


class StudentModelAdmin(BaseUserAdmin):
    inlines = [StudentMoreTabularInline]

    # class Meta:
    #     model = Student

    list_display = ("email", "name")
    # raw_id_fields = ["user"]
    list_filter = ("is_admin",)
    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email", "id")
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)
admin.site.register(Admin, AdminModelAdmin)
admin.site.register(Teacher, TeacherModelAdmin)
admin.site.register(Student, StudentModelAdmin)
