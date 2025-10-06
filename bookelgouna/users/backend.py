# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model


class TravelAgencyAuthBackend(object):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, user_pk, current_user, **kwargs):
        if user_pk != current_user.pk:
            UserModel = get_user_model()
            try:
                user = UserModel._default_manager.get(pk=user_pk)
            except UserModel.DoesNotExist:
                pass
            else:
                if user.is_business_related_user():
                    if current_user.is_travel_agency() and user in current_user.subaccounts.all():
                        # check if user in subaccounts
                        return user
                    else:  # is_business_owner
                        # check if user in subaccounts or is base account
                        base_account = current_user.base_account
                        if user in base_account.subaccounts.all() or user == base_account:
                            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

