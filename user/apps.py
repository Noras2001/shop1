from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

#    def ready(self):
        # Aquí podrías importar signals o hacer otra configuración
#        import user.signals

