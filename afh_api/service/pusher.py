import pusher
from django.conf import settings

pusher_client = pusher.Pusher(**settings.PUSHER_CONFIG)