from django.apps import AppConfig


class StoreApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store_api'

    def ready(self) -> None:
        import store_api.signals
        return super().ready()
