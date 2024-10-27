from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.user_profile'

    def ready(self):
        import api.user_profile.signals  