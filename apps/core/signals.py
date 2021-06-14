from datetime import datetime, date
from decimal import Decimal

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.models import HelpDesk, Message
from apps.core.serializers import HelpDeskSerializer, MessageSerializer


def serialize_anything(data):
    for key, _ in data.items():
        if isinstance(data[key], datetime) or isinstance(data[key], date) or isinstance(data[key], Decimal):
            data[key] = str(data[key])
    return data


@receiver(post_save, sender=HelpDesk)
def update_helpdesk(sender, instance, created, **kwargs):
    data = serialize_anything(HelpDeskSerializer(instance=instance).data)
    type_ = "update_helpdesk"
    channel_layer = get_channel_layer()
    group_name = f'chat_room'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': type_,
            'data': data,
        }
    )


@receiver(post_save, sender=Message)
def update_message(sender, instance, created, **kwargs):
    data = serialize_anything(MessageSerializer(instance=instance).data)
    type_ = "update_message"
    if created:
        type_ = "new_message"
    channel_layer = get_channel_layer()
    group_name = f'organization_{instance.organization}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': type_,
            'data': data,
        }
    )

