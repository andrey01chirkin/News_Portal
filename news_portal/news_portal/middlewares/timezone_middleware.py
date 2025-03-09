import pytz
from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and "timezone" in request.POST:
            request.session['django_timezone'] = request.POST['timezone']

        tzname = request.session.get('django_timezone', 'Europe/Moscow')
        timezone.activate(pytz.timezone(tzname))

        return self.get_response(request)
