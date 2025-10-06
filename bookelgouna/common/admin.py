from django.contrib import admin
from django.utils.encoding import force_str

from .models import Service, Language, TempFile, ReservationPhoneSettings
from users.models import BusinessOwnerInfo


class ApproveServiceAfterSaveMixin(object):
    """Should be used with ModelAdmin of unapproved objects subset only (UnapprovedHotel, UnapprovedRoom and so on)"""
    def response_change(self, request, obj):
        if obj.status == Service.APPROVED:
            obj.rewrite_origin_object_with_approved_duplicate(obj.origin, obj)
        elif obj.status == Service.REJECTED:
            pass
            # obj.remove_duplicate(obj.origin, obj)
        return super(ApproveServiceAfterSaveMixin, self).response_change(request, obj)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'is_enabled')


admin.site.register(Language, LanguageAdmin)


class TempFileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'created')


admin.site.register(TempFile, TempFileAdmin)


class ReservationPhoneAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'get_enabled_for_services', 'is_enabled')
    list_editable = ('is_enabled',)

    def get_enabled_for_services(self, obj):
        types = dict(BusinessOwnerInfo.SERVICE_TYPES)
        return u', '.join([force_str(types[int(t)]) for t in obj.enabled_for_services])
    get_enabled_for_services.short_description = 'Enabled for services'

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        else:
            return True

admin.site.register(ReservationPhoneSettings, ReservationPhoneAdmin)
