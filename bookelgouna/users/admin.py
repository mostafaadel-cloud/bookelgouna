# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress

from django import forms
import django
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import User, BusinessOwnerInfo, Country
from users.admin_views import TravelAgencyCreateView


class CountryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'get_default_language_display')


class MyUserChangeForm(UserChangeForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class BusinessOwnerInline(admin.StackedInline):
    model = BusinessOwnerInfo


class TravelAgencyInlineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TravelAgencyInlineForm, self).__init__(*args, **kwargs)
        self.fields['allowed_types'].required = True

    class Meta:
        model = BusinessOwnerInfo
        fields = ('allowed_types',)



class TravelAgencyInfoInline(admin.StackedInline):
    model = BusinessOwnerInfo
    form = TravelAgencyInlineForm
    can_delete = False
    verbose_name = 'Travel Agency Info'
    verbose_name_plural = 'Travel Agency Info'


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    change_list_template = "users/admin/users_change_list.html"

    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff', 'type_details',
                    'related_travel_agency', 'country')
    fieldsets = (
        (None, {'fields': ('username', 'related_travel_agency', 'type', 'password')}),
        (_('Personal info'), {'fields': ('avatar', 'first_name', 'last_name', 'email', 'preferred_language', 'country', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('related_travel_agency',)
    business_owner_inlines = [BusinessOwnerInline]
    travel_agency_inlines = [TravelAgencyInfoInline]

    def type_details(self, obj):
        t = obj.get_type_display()
        if obj.is_end_user():
            return t
        elif obj.is_business_owner():
            return "%s (%s)" % (obj.get_type_display(), obj.get_service_type_full_name())
        else:
            return obj.get_type_display()

    def related_travel_agency(self, obj):
        if obj.is_business_owner() and obj.base_account:
            return "<a href='%s'>%s</a>" % (reverse('admin:users_user_change', args=(obj.base_account.pk,)),
                                            obj.base_account.username)
        return '-'
    related_travel_agency.allow_tags = True

    def get_inline_instances(self, request, obj=None):
        if obj and obj.is_business_owner():
            inlines = self.business_owner_inlines
        elif obj and obj.is_travel_agency():
            inlines = self.travel_agency_inlines
        else:
            inlines = self.inlines
        inline_instances = []
        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_add_permission(request) or
                        inline.has_change_permission(request, obj) or
                        inline.has_delete_permission(request, obj)):
                    continue
                if not inline.has_add_permission(request):
                    inline.max_num = 0
            inline_instances.append(inline)
        return inline_instances

    def get_urls(self):
        return patterns('', url(r'^add_travel_agency/$', self.admin_site.admin_view(TravelAgencyCreateView.as_view()),
                                name='add_travel_agency')) + super(MyUserAdmin, self).get_urls()

    class Media:
        js = ('js/admin/deactivate_user.js',)


class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'primary', 'verified')
    list_filter = ('primary', 'verified')
    search_fields = []
    raw_id_fields = ('user',)

    def __init__(self, *args, **kwargs):
        super(EmailAddressAdmin, self).__init__(*args, **kwargs)
        if not self.search_fields and django.VERSION[:2] < (1, 7):
            self.search_fields = self.get_search_fields(None)

    def get_search_fields(self, request):
        base_fields = get_adapter().get_user_search_fields()
        return ['email'] + list(map(lambda a: 'user__' + a, base_fields))

    class Media:
        js = ('js/admin/set_email_as_verified.js',)



admin.site.register(Country, CountryAdmin)
admin.site.register(User, MyUserAdmin)
admin.site.unregister(EmailAddress)
admin.site.register(EmailAddress, EmailAddressAdmin)
