# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from aggregate_if import Count
from allauth.account import app_settings
from allauth.account.forms import LoginForm, ChangePasswordForm, SetPasswordForm
from allauth.account.views import SignupView, LoginView, RedirectAuthenticatedUserMixin, ConfirmEmailView, \
    PasswordResetView, PasswordResetFromKeyView, sensitive_post_parameters_m, _ajax_response
from allauth.utils import get_form_class
from braces.views import LoginRequiredMixin, SelectRelatedMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Prefetch, Q
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_text
from django.utils.translation import pgettext
from django.views.generic import View, TemplateView, UpdateView, FormView, ListView, CreateView

from booking.forms import OfflineBookingForm
from booking.models import Order, OrderItem
from common.mixins import JsonMixin
from common.utils import get_phone_prefix_or_empty_string_for

from .mixins import BusinessOwnerOnlyMixin, EndUserOnlyMixin, EndUserProfileTabMixin, BusinessProfileTabMixin, \
    BusinessRelatedUserMixin
from .exceptions import WrongUserType
from .forms import BusinessSignupForm, BusinessLoginForm, BusinessResetPasswordForm, EndUserProfileEditForm, \
    BusinessProfileEditForm, SubaccountForm
from .models import User, BusinessOwnerInfo
from .utils import get_country_code_by_ip_using_geoip


class BusinessLoginView(LoginView):
    template_name = "users/includes/business_login.html"
    form_class = BusinessLoginForm
    redirect_url_if_wrong_user_type = reverse_lazy('account_login')

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, 'business_login', self.form_class)

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(BusinessLoginView, self).dispatch(request, *args, **kwargs)
        except WrongUserType:
            messages.warning(request, pgettext('end user uses incorrect form to login notification',
                                               'You are a tourist. You should use this form to login.'))
            return _ajax_response(request, HttpResponseRedirect(self.redirect_url_if_wrong_user_type))

business_login = BusinessLoginView.as_view()


class BusinessSignupView(SignupView):
    template_name = "users/includes/business_signup.html"
    form_class = BusinessSignupForm

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, 'business_signup', self.form_class)

business_signup = BusinessSignupView.as_view()


class BusinessLoginSignupView(RedirectAuthenticatedUserMixin, TemplateView):
    template_name = "users/business.html"
    redirect_field_name = "next"
    success_url = reverse_lazy('choose_profile')

    def get_success_url(self):
            """
            Returns the supplied success URL.
            """
            if self.success_url:
                # Forcing possible reverse_lazy evaluation
                url = force_text(self.success_url)
            else:
                raise ImproperlyConfigured(
                    "No URL to redirect to. Provide a success_url.")
            return url

    def get_context_data(self, **kwargs):
        context = super(BusinessLoginSignupView, self).get_context_data(**kwargs)
        context['login_form'] = BusinessLoginForm()
        context['signup_form'] = BusinessSignupForm()
        context['redirect_field_name'] = self.redirect_field_name
        redirect_field_value = self.request.REQUEST.get(self.redirect_field_name)
        context['redirect_field_value'] = redirect_field_value
        return context

business = BusinessLoginSignupView.as_view()


class UserLoginView(LoginView):
    redirect_url_if_wrong_user_type = reverse_lazy('business')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(UserLoginView, self).dispatch(request, *args, **kwargs)
        except WrongUserType:
            messages.warning(request, pgettext('business owner uses incorrect form to login notification',
                                               'You are a business owner. You should use this form to login.'))
            return HttpResponseRedirect(self.redirect_url_if_wrong_user_type)


user_login = UserLoginView.as_view()


class UserSignupView(SignupView):
    def get_initial(self):
        initial = super(UserSignupView, self).get_initial()

        if self.request.method == 'GET':
            country_code = get_country_code_by_ip_using_geoip(self.request)
            if country_code:
                initial['country'] = country_code
                initial['phone'] = get_phone_prefix_or_empty_string_for(country_code)
        return initial


user_signup = UserSignupView.as_view()


class ChooseProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_business_related_user():
            return HttpResponseRedirect(reverse('business_profile'))
        else:
            return HttpResponseRedirect(reverse('user_profile'))

choose_profile = ChooseProfileView.as_view()


class AccountEmailVerificationView(TemplateView):
    template_name = "users/user_verification_sent.html"

    def dispatch(self, request, *args, **kwargs):
        if 'HTTP_REFERER' in request.META and 'business' in request.META['HTTP_REFERER']:
            return HttpResponseRedirect(reverse('business_email_verification_sent'))
        return super(AccountEmailVerificationView, self).dispatch(request, *args, **kwargs)

account_email_verification = AccountEmailVerificationView.as_view()


class BusinessConfirmEmail(ConfirmEmailView):

    def get_template_names(self):
        return ["users/business_email_confirm.html"]

business_confirm_email = BusinessConfirmEmail.as_view()


class BusinessPasswordReset(PasswordResetView):
    template_name = "users/business_password_reset.html"
    form_class = BusinessResetPasswordForm
    success_url = reverse_lazy("business_reset_password_done")

business_password_reset = BusinessPasswordReset.as_view()


class BusinessPasswordResetFromKey(PasswordResetFromKeyView):
    template_name = "users/business_password_reset_from_key.html"
    success_url = reverse_lazy("business_reset_password_from_key_done")

business_password_reset_from_key = BusinessPasswordResetFromKey.as_view()


class UserProfileView(EndUserOnlyMixin, EndUserProfileTabMixin, JsonMixin, TemplateView):
    tab_name = "profile"
    ajax_template_name = "users/includes/ajax_user_profile_tab_view_profile.html"

user_profile = UserProfileView.as_view()


class EditEndUserProfile(EndUserOnlyMixin, EndUserProfileTabMixin, JsonMixin, UpdateView):
    tab_name = "profile"
    model = User
    form_class = EndUserProfileEditForm
    ajax_template_name = "users/includes/ajax_user_profile_tab_edit_profile.html"
    success_url = reverse_lazy('user_profile')

    def get_initial(self):
        initial = super(EditEndUserProfile, self).get_initial()

        if self.request.method == 'GET':
            country = self.object.country
            phone = self.object.phone
            if country and country.code and phone is None:
                initial['phone'] = get_phone_prefix_or_empty_string_for(country.code)
        return initial

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'avatar' in form.changed_data:
            self.object.cropping = None
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

edit_end_user_profile = EditEndUserProfile.as_view()


class ChangeEndUserPasswordView(EndUserOnlyMixin, EndUserProfileTabMixin, JsonMixin, FormView):
    tab_name = "profile"
    form_class = ChangePasswordForm
    ajax_template_name = "users/includes/ajax_user_profile_tab_change_pass.html"
    success_url = reverse_lazy("user_profile")

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, 'end_user_change_password', self.form_class)

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_usable_password():
            return HttpResponseRedirect(reverse('account_set_password'))
        return super(ChangeEndUserPasswordView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ChangeEndUserPasswordView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()

        # allauth signal:
        # from allauth.account import signals
        # signals.password_changed.send(sender=self.request.user.__class__,
        #                               request=self.request,
        #                               user=self.request.user)
        return super(ChangeEndUserPasswordView, self).form_valid(form)

change_end_user_password = ChangeEndUserPasswordView.as_view()


class SetEndUserPasswordView(EndUserOnlyMixin, EndUserProfileTabMixin, JsonMixin, FormView):
    tab_name = "profile"
    ajax_template_name = "users/includes/ajax_user_profile_tab_set_pass.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy("user_profile")

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, 'end_user_set_password', self.form_class)

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_usable_password():
            return HttpResponseRedirect(reverse('account_change_password'))
        return super(SetEndUserPasswordView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SetEndUserPasswordView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # get_adapter().add_message(self.request,
        #                           messages.SUCCESS,
        #                           'account/messages/password_set.txt')
        # signals.password_set.send(sender=self.request.user.__class__,
        #                           request=self.request, user=self.request.user)
        return super(SetEndUserPasswordView, self).form_valid(form)

set_end_user_password = SetEndUserPasswordView.as_view()


class BusinessDashboardView(BusinessRelatedUserMixin, BusinessProfileTabMixin, JsonMixin, TemplateView):
    tab_name = "dashboard"
    ajax_template_name = "users/includes/ajax_business_profile_tab_dashboard_view.html"

    def get_context_data(self, **kwargs):
        context = super(BusinessDashboardView, self).get_context_data(**kwargs)
        base_account = self.request.user.get_base_account_or_self()
        all_types = dict(BusinessOwnerInfo.SERVICE_TYPES)
        allowed_types = [int(t) for t in base_account.business_info.allowed_types]
        subaccounts = base_account.subaccounts.prefetch_related('business_info').annotate(
            bookings=Count('order_items', only=Q(order_items__status=OrderItem.PENDING)))
        type2subaccounts = {}
        for t in allowed_types:
            type2subaccounts[t] = {'name': all_types[t], 'items': []}
        for subacc in subaccounts:
            type2subaccounts[subacc.business_info.service_type]['items'].append(subacc)
        context['base_account'] = base_account
        context['grouped_subaccounts'] = type2subaccounts
        return context

    # TODO: travel agencies AND business owners if only base_account.exists()


business_dashboard = BusinessDashboardView.as_view()


class LoginAsView(BusinessRelatedUserMixin, View):
    def get(self, request, *args, **kwargs):
        user_pk = request.GET.get('user_pk')
        try:
            user_pk = int(user_pk)
        except ValueError:
            raise PermissionDenied()
        auth_user = authenticate(user_pk=user_pk, current_user=request.user)
        if auth_user is None:
            raise PermissionDenied()
        login(self.request, auth_user)
        data = {
            'reload': True
        }
        if auth_user.is_travel_agency():
            url = reverse('business_dashboard')
        else:
            url = reverse('service_view')
        data['url'] = url
        return JsonResponse(data)

business_login_as = LoginAsView.as_view()


class AddSubaccountView(BusinessRelatedUserMixin, BusinessProfileTabMixin, JsonMixin, CreateView):
    tab_name = "dashboard"
    ajax_template_name = "users/includes/ajax_business_profile_tab_dashboard_create_subacc.html"
    form_class = SubaccountForm

    def get_initial(self):
        initial = super(AddSubaccountView, self).get_initial()
        service_type = int(self.kwargs.get('pk'))
        if service_type not in dict(BusinessOwnerInfo.SERVICE_TYPES):
            raise Http404()
        initial['service_type'] = service_type
        return initial

    def get_form_kwargs(self):
        kwargs = super(AddSubaccountView, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AddSubaccountView, self).get_context_data(**kwargs)
        service_type = int(self.kwargs.get('pk'))
        context['service_type_pk'] = service_type
        context['service_type_name'] = dict(BusinessOwnerInfo.SERVICE_TYPES).get(service_type)
        return context

    def form_valid(self, form):
        user = form.save()
        auth_user = authenticate(user_pk=user.pk, current_user=self.request.user)
        if auth_user is None:
            raise PermissionDenied()
        login(self.request, auth_user)
        data = {
            'reload': True
        }
        url = reverse('create_service')
        data['url'] = url
        return JsonResponse(data)


business_add_subaccount = AddSubaccountView.as_view()


class BusinessProfileView(BusinessRelatedUserMixin, BusinessProfileTabMixin, JsonMixin, TemplateView):
    tab_name = "profile"
    ajax_template_name = "users/includes/ajax_business_profile_tab_view_profile.html"

    def get_context_data(self, **kwargs):
        context = super(BusinessProfileView, self).get_context_data(**kwargs)
        context['business_user'] = self.request.user.get_base_account_or_self()
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(BusinessProfileView, self).get_context_data(**kwargs)
    #     services_manager = self.request.user.services
    #     context['has_services'] = services_manager.exists()
    #     if services_manager.exists():
    #         context['items'] = self.request.user.get_original_service().get_all_original_items()
    #     # if services_manager.exists():
    #     #     context['services'] = services_manager.filter(Q(origin__isnull=True, duplicate__isnull=True) |  # originals
    #     #                                                   Q(origin__isnull=False, duplicate__isnull=True))  # duplicates
    #     return context

business_profile = BusinessProfileView.as_view()


class EditBusinessProfile(BusinessRelatedUserMixin, BusinessProfileTabMixin, JsonMixin, UpdateView):
    tab_name = "profile"
    model = User
    form_class = BusinessProfileEditForm
    ajax_template_name = "users/includes/ajax_business_profile_tab_edit_profile.html"
    success_url = reverse_lazy('business_profile')

    def get_context_data(self, **kwargs):
        context = super(EditBusinessProfile, self).get_context_data(**kwargs)
        context['business_user'] = self.request.user.get_base_account_or_self()
        return context

    def get_object(self, queryset=None):
        user = self.request.user.get_base_account_or_self()
        return user

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'avatar' in form.changed_data:
            self.object.cropping = None
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


edit_business_profile = EditBusinessProfile.as_view()


class ChangeBusinessPasswordView(BusinessRelatedUserMixin, BusinessProfileTabMixin, JsonMixin, FormView):
    tab_name = "profile"
    form_class = ChangePasswordForm
    ajax_template_name = "users/includes/ajax_business_profile_tab_change_pass.html"
    success_url = reverse_lazy('business_profile')

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, 'business_change_password', self.form_class)

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_usable_password():
            return HttpResponseRedirect(reverse('account_set_password'))
        return super(ChangeBusinessPasswordView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ChangeBusinessPasswordView, self).get_form_kwargs()
        kwargs["user"] = self.request.user.get_base_account_or_self()
        return kwargs

    def form_valid(self, form):
        form.save()

        # allauth signal:
        # from allauth.account import signals
        # signals.password_changed.send(sender=self.request.user.__class__,
        #                               request=self.request,
        #                               user=self.request.user)
        return super(ChangeBusinessPasswordView, self).form_valid(form)

change_business_password = ChangeBusinessPasswordView.as_view()


class UserBillingView(EndUserOnlyMixin, EndUserProfileTabMixin, JsonMixin, TemplateView):
    tab_name = "billing"
    ajax_template_name = "users/includes/ajax_user_profile_tab_billing.html"

user_billing = UserBillingView.as_view()


class BusinessBillingView(BusinessRelatedUserMixin, BusinessProfileTabMixin, JsonMixin, TemplateView):
    tab_name = "billing"
    ajax_template_name = "users/includes/ajax_business_profile_tab_billing.html"

    def get_context_data(self, **kwargs):
        context = super(BusinessBillingView, self).get_context_data(**kwargs)
        context['business_user'] = self.request.user.get_base_account_or_self()
        return context

business_billing = BusinessBillingView.as_view()


class ServiceView(BusinessOwnerOnlyMixin, JsonMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.has_service():
            return HttpResponseRedirect(reverse('items_list'))
        else:
            return HttpResponseRedirect(reverse('create_service'))

service_view = ServiceView.as_view()


class EndUserBookings(EndUserOnlyMixin, EndUserProfileTabMixin, JsonMixin, ListView):
    tab_name = "bookings"
    ajax_template_name = "users/includes/ajax_user_profile_tab_my_bookings.html"
    model = Order

    def get_queryset(self):
        return self.request.user.orders.prefetch_related(
            Prefetch('items', OrderItem.objects.prefetch_related('content_type', 'owner').order_by('content_type')))\
            .order_by('-date_created')


user_bookings = EndUserBookings.as_view()


class BusinessBookings(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, ListView):
    tab_name = "bookings"
    ajax_template_name = "users/includes/ajax_business_profile_tab_my_bookings.html"
    model = OrderItem

    def get_queryset(self):
        q = self.request.user.order_items.select_related('order__user').prefetch_related(
            'content_object', 'content_type'
        ).order_by('-order__date_created')
        return q

business_bookings = BusinessBookings.as_view()


class CreateOfflineBooking(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, CreateView):
    tab_name = "bookings"
    ajax_template_name = "users/includes/ajax_business_profile_tab_create_offline_booking.html"
    form_class = OfflineBookingForm
    success_url = reverse_lazy('business_bookings')

    def get_form_kwargs(self):
        # pass "user" keyword argument with the current user to your form
        kwargs = super(CreateOfflineBooking, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        apt = form.cleaned_data['apartment']
        price_category = apt.price_category
        self.object.owner = self.request.user
        self.object.order = Order.objects.create()
        self.object.content_type = ContentType.objects.get_for_model(price_category)
        self.object.object_id = price_category.pk
        self.object.mark_as_offline(commit=False)
        self.object.quantity = 1
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        # enable this page access for apartment business owners only
        if request.user.is_authenticated() and request.user.is_business_owner() and not request.user.is_apt_owner():
            return HttpResponseRedirect(self.get_success_url())
        return super(CreateOfflineBooking, self).dispatch(request, *args, **kwargs)


business_create_offline_booking = CreateOfflineBooking.as_view()


class BusinessDocsView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, TemplateView):
    tab_name = "docs"
    ajax_template_name = "users/includes/ajax_business_profile_tab_docs.html"

business_docs = BusinessDocsView.as_view()


class BusinessStatisticsView(BusinessRelatedUserMixin, BusinessProfileTabMixin, JsonMixin, TemplateView):
    tab_name = "stats"
    ajax_template_name = "users/includes/ajax_business_profile_tab_statistics.html"

    def get_context_data(self, **kwargs):
        context = super(BusinessStatisticsView, self).get_context_data(**kwargs)
        context['business_user'] = self.request.user.get_base_account_or_self()
        return context

business_statistics = BusinessStatisticsView.as_view()
