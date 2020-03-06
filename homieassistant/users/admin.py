from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

from . import models


class TokenInline(admin.StackedInline):
    verbose_name = "Authentication token"
    verbose_name_plural = "Authentication tokens"
    model = Token
    extra = 0
    fields = ("key", "created")
    readonly_fields = ("created",)


@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        ("User", {"fields": ("email", "password")}),
        (_("Personal"), {"fields": ("first_name", "last_name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "created_at", "updated_at",)},
        ),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    exclude = ("username",)
    list_display = ("email", "first_name", "last_name", "created_at")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines = (TokenInline,)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields
        return self.readonly_fields
