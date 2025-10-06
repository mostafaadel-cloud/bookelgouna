# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from allauth.account import app_settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import resolve_url
from django.utils.translation import pgettext

from common.utils import download_file_from_url

from .forms import BusinessSignupForm
from .models import User, BusinessOwnerInfo, Country


class AccountAdapter(DefaultAccountAdapter):

    def render_mail(self, template_prefix, email, context):
        """
        Replace activate url if the user is business owner and mail is email confirmation.
        """
        if 'account/email/email_confirmation' in template_prefix:
            user = context['user']
            if user.is_business_owner():
                key = context['key']
                enduser_full_activate_url = context['activate_url']
                enduser_activate_url = reverse("account_confirm_email", args=[key])
                business_activate_url = reverse("business_confirm_email", args=[key])
                business_full_activate_url = enduser_full_activate_url.replace(enduser_activate_url, business_activate_url)
                context['activate_url'] = business_full_activate_url
        return super(AccountAdapter, self).render_mail(template_prefix, email, context)

    def get_email_confirmation_redirect_url(self, request):
        if request.user.is_authenticated():
            return super(AccountAdapter, self).get_email_confirmation_redirect_url(request)
        else:
            if 'HTTP_REFERER' in request.META and 'business' in request.META['HTTP_REFERER']:
                return 'business'
            else:
                return app_settings.EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL

    def save_user(self, request, user, form, commit=True):
        user = super(AccountAdapter, self).save_user(request, user, form, commit=False)
        data = form.cleaned_data
        user.phone = data.get('phone')
        is_business_owner = False
        if isinstance(form, BusinessSignupForm):
            is_business_owner = True
            user.type = User.BUSINESS_OWNER
            user.country = 'EG'  # always Egypt here
        else:
            # enduser
            user.country = data.get('country')
        user.preferred_language = getattr(request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
        user.save()
        if is_business_owner:
            BusinessOwnerInfo.objects.create(user=user, service_type=data.get('service_type'))
        return user

    def get_logout_redirect_url(self, request):
        u = request.user
        if u.is_authenticated() and u.is_business_related_user():
            return resolve_url(settings.OWNER_LOGOUT_REDIRECT_URL)
        else:
            return super(AccountAdapter, self).get_logout_redirect_url(request)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)
        user.preferred_language = getattr(request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
        user.save()

        url = sociallogin.account.get_avatar_url()

        avatar = download_file_from_url(url)
        if avatar:
            # hardcoded here format cause Facebook transforms other image formats into jpg (tested with png)
            user.avatar.save('avatar%d.jpg' % user.pk, avatar)

        messages.info(request, pgettext('facebook user notification to add phone',
        'You should add your phone via profile edit form. Click <a class="%(css)s" href="%(url)s">here</a> to do this now.'
                                        % {'css': 'popup_link', 'url': reverse('edit_user_profile')}))

        return user
