from skd_tools.mixins import ActiveTabMixin

from django.views.generic import TemplateView

from common.forms import DatesAndGuestsPostForm
from weatherapi.utils import get_current_weather_info


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        initial = {}
        required_keys = ['arrival', 'departure', 'adults', 'children']
        if all([key in self.request.session for key in required_keys]):
            initial = {key: self.request.session[key] for key in required_keys}
        else:
            initial = DatesAndGuestsPostForm.default_data()

        context['index_dates_and_guests_form'] = DatesAndGuestsPostForm(prefix='index', initial=initial)
        return context


index = IndexView.as_view()


class WeatherView(ActiveTabMixin, TemplateView):
    active_tab = 'weather'
    template_name = 'core/weather.html'

    def get_context_data(self, **kwargs):
        context = super(WeatherView, self).get_context_data(**kwargs)
        context['weather_info'] = get_current_weather_info()
        return context

weather = WeatherView.as_view()
