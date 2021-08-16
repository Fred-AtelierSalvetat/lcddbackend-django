from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Keyword, Link, RefLegifrance, Topic, Workshop, UserProfile, Profession
from django import forms


class KeywordInline(admin.TabularInline):
    model = Keyword


class LinkInline(admin.TabularInline):
    model = Link


class WorkshopAdmin(admin.ModelAdmin):
    model = Workshop
    inlines = [
        KeywordInline,
        LinkInline,
    ]


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")
        return self.cleaned_data["last_name"]

    def clean_email(self):
        if self.cleaned_data["email"].strip() == '':
            raise ValidationError("Email is required.")
        return self.cleaned_data["email"]


class UserAdmin(BaseUserAdmin):
    form = MyUserChangeForm
    inlines = (UserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profession)
admin.site.register(Topic)
admin.site.register(RefLegifrance)
admin.site.register(Workshop, WorkshopAdmin)
