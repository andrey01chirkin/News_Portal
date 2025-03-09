import pytz
from django.utils import timezone


def timezone_context(request):
    """Добавляет информацию о часовом поясе и текущем времени в контекст всех шаблонов."""
    selected_timezone = request.session.get('django_timezone', 'Europe/Moscow')
    user_tz = pytz.timezone(selected_timezone)

    # Получаем текущее время в выбранном пользователем часовом поясе
    current_time = timezone.now().astimezone(user_tz)

    return {
        'selected_timezone': selected_timezone,
        'timezones': pytz.common_timezones,
        'current_time': current_time,  # Передаём текущее время глобально
        'current_hour': current_time.hour,  # Передаём час отдельно
    }
