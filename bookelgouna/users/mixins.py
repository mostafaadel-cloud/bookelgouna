# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import wraps
from django.contrib.auth.decorators import user_passes_test

from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str


def redirect_if_incorrect_type(test_func, redirect_to):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated() and test_func(request.user):
                return view_func(request, *args, **kwargs)
            resolved_redirect_url = force_str(resolve_url(redirect_to))
            return HttpResponseRedirect(resolved_redirect_url)
        return wrapper
    return decorator


class EndUserOnlyMixin(object):
    """
    View mixin which verifies that the user is end user.
    """
    @method_decorator(user_passes_test(lambda u: u.is_authenticated(), login_url='account_login'))
    @method_decorator(redirect_if_incorrect_type(lambda u: u.is_end_user(), redirect_to='business_profile'))
    def dispatch(self, request, *args, **kwargs):
        return super(EndUserOnlyMixin, self).dispatch(request, *args, **kwargs)


class BusinessOwnerOnlyMixin(object):
    """
    View mixin which verifies that the user is business owner.
    """
    @method_decorator(user_passes_test(lambda u: u.is_authenticated(), login_url='business'))
    @method_decorator(redirect_if_incorrect_type(lambda u: u.is_business_owner(), redirect_to='user_profile'))
    def dispatch(self, request, *args, **kwargs):
        return super(BusinessOwnerOnlyMixin, self).dispatch(request, *args, **kwargs)


class BusinessRelatedUserMixin(object):
    """
    View mixin which verifies that the user is business owner OR travel agency.
    """
    @method_decorator(user_passes_test(lambda u: u.is_authenticated(), login_url='business'))
    @method_decorator(redirect_if_incorrect_type(lambda u: u.is_business_related_user(), redirect_to='user_profile'))
    def dispatch(self, request, *args, **kwargs):
        return super(BusinessRelatedUserMixin, self).dispatch(request, *args, **kwargs)


class ProfileTabMixin(object):
    tab_name = None
    ajax_template_name = None

    def get_ajax_template_names(self):
        if self.ajax_template_name:
            return [self.ajax_template_name]
        else:
            return super(ProfileTabMixin, self).get_ajax_template_names()

    def get_template_names(self):
        if self.request.is_ajax():
            return self.get_ajax_template_names()
        return [self.template_name]

    def get_tabs(self):
        user = self.request.user
        if user.is_end_user():
            prefix = 'users/includes/user_tabs/'
            tabs = ['profile', 'billing', 'bookings']
        elif user.is_business_owner():
            prefix = 'users/includes/business_tabs/'
            tabs = ['profile', 'billing', 'service', 'bookings', 'docs', 'stats']
            if user.base_account is not None:
                tabs.insert(0, 'dashboard')
        elif user.is_travel_agency():
            prefix = 'users/includes/business_tabs/'
            tabs = ['dashboard', 'profile', 'billing', 'stats']
        self.tabs = tabs
        return ['{}{}.html'.format(prefix, tab) for tab in tabs]

    def get_context_data(self, **kwargs):
        context = super(ProfileTabMixin, self).get_context_data(**kwargs)
        context['tab_name'] = self.tab_name
        context['tabs'] = self.get_tabs()
        context['ajax_template_name'] = self.get_ajax_template_names()[0]
        return context


class EndUserProfileTabMixin(ProfileTabMixin):
    template_name = "users/user_profile_tab.html"


class BusinessProfileTabMixin(ProfileTabMixin):
    template_name = "users/business_profile_tab.html"

    def get_context_data(self, **kwargs):
        context = super(BusinessProfileTabMixin, self).get_context_data(**kwargs)
        if 'service' in self.tabs:
            context['service_type'] = self.request.user.get_service_type_full_name()
        return context
