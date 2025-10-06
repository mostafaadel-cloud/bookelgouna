from allauth.account.models import EmailAddress
from braces.views import SuperuserRequiredMixin, CsrfExemptMixin
from django.core.urlresolvers import reverse_lazy

from django.http import JsonResponse
from django.views.generic import View, CreateView

from .admin_forms import TravelAgencyForm
from .models import User


class DeactivateAccountView(CsrfExemptMixin, SuperuserRequiredMixin, View):

    def post(self, *args, **kwargs):
        data = {
            'status': 'fail'
        }
        user_pk = kwargs.get('pk', None)

        if user_pk:
            user = User.objects.get(pk=user_pk)
            if user.is_active:
                user.is_active = False
                user.save()
                data['status'] = 'success'

        if data['status'] == 'fail':
            data['message'] = 'internal server error'

        return JsonResponse(data)

deactivate_account = DeactivateAccountView.as_view()


class SetEmailAsVerifiedView(CsrfExemptMixin, SuperuserRequiredMixin, View):

    def post(self, *args, **kwargs):
        data = {
            'status': 'fail'
        }
        email_pk = kwargs.get('pk', None)

        if email_pk:
            email = EmailAddress.objects.get(pk=email_pk)
            if not email.verified:
                email.verified = True
                email.save()
                data['status'] = 'success'

        if data['status'] == 'fail':
            data['message'] = 'internal server error'

        return JsonResponse(data)

set_email_as_verified = SetEmailAsVerifiedView.as_view()


class TravelAgencyCreateView(SuperuserRequiredMixin, CreateView):
    template_name = 'users/admin/create_travel_agency.html'
    form_class = TravelAgencyForm
    success_url = reverse_lazy('admin:users_user_changelist')
