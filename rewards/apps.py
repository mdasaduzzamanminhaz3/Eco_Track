from django.apps import AppConfig


class RewardsConfig(AppConfig):
    name = 'rewards'
    def ready(self):
        import rewards.signals  # Import signals to connect them