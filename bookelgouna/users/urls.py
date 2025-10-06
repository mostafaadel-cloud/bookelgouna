from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.utils.six import wraps

from . import views, admin_views

def signin_wrapper(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        request.old_cart_id = request.cart.id
        return func(request, *args, **kwargs)

    return wrapper

signin = signin_wrapper(views.user_login)


urlpatterns = patterns('',
    url(r'^admin/accounts/deactivate/(?P<pk>\d+)/$', admin_views.deactivate_account, name='deactivate_account'),
    url(r'^admin/accounts/set_email_as_verified/(?P<pk>\d+)/$', admin_views.set_email_as_verified,
        name='set_email_as_verified'),
    url(r'^accounts/choose_profile/$', views.choose_profile, name='choose_profile'),
    url(r'^accounts/profile/$', views.user_profile, name='user_profile'),
    url(r"^accounts/login/$", signin, name="account_login"),
    url(r'^accounts/signup/$', views.user_signup, name='account_signup'),
    url(r'^accounts/edit_profile/$', views.edit_end_user_profile, name='edit_user_profile'),
    url(r'^accounts/password/change/$', views.change_end_user_password, name='account_change_password'),
    url(r'^accounts/password/set/$', views.set_end_user_password, name='account_set_password'),
    url(r'^accounts/billing/$', views.user_billing, name='user_billing'),
    url(r'^accounts/bookings/$', views.user_bookings, name='user_bookings'),
    url(r'^business/dashboard/$', views.business_dashboard, name='business_dashboard'),
    url(r'^business/login_as/$', views.business_login_as, name='business_login_as'),
    url(r'^business/add_subaccount/(?P<pk>\d+)/$', views.business_add_subaccount, name='business_add_subaccount'),
    url(r'^business/profile/$', views.business_profile, name='business_profile'),
    url(r'^business/edit_profile/$', views.edit_business_profile, name='edit_business_profile'),
    url(r'^business/password/change/$', views.change_business_password, name='business_change_password'),
    url(r'^business/billing/$', views.business_billing, name='business_billing'),
    url(r'^business/bookings/$', views.business_bookings, name='business_bookings'),
    url(r'^business/bookings/create/$', views.business_create_offline_booking, name='business_create_offline_booking'),
    url(r'^business/docs/$', views.business_docs, name='business_docs'),
    url(r'^business/statistics/$', views.business_statistics, name='business_statistics'),
    url(r'^business/service_view/$', views.service_view, name='service_view'),
    url(r'^business/$', views.business, name='business'),
    url(r'^business_login/$', views.business_login, name='business_login'),
    url(r'^business_signup/$', views.business_signup, name='business_signup'),

    url(r"^business/confirm-email/$", TemplateView.as_view(template_name="users/business_verification_sent.html"),
        name="business_email_verification_sent"),
    url(r"^accounts/confirm-email/$", views.account_email_verification,
        name="account_email_verification_sent"),
    url(r"^business/confirm-email/(?P<key>\w+)/$", views.business_confirm_email,
        name="business_confirm_email"),
    #
    # # password reset
    url(r"^business/password/reset/$", views.business_password_reset,
        name="business_reset_password"),
    url(r"^business/password/reset/done/$", TemplateView.as_view(template_name="users/business_password_reset_done.html"),
        name="business_reset_password_done"),
    url(r"^business/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.business_password_reset_from_key,
        name="business_reset_password_from_key"),
    url(r"^business/password/reset/key/done/$", TemplateView.as_view(template_name="users/business_password_reset_from_key_done.html"),
        name="business_reset_password_from_key_done"),
)
