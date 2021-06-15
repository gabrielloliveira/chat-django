from rest_framework import serializers

from apps.core.models import HelpDesk, Message, Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ("id", )


class HelpDeskSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = HelpDesk
        fields = ("created_at", "updated_at", "uuid", "client", "last_message",)

    def get_last_message(self, help_desk: HelpDesk):
        last_message = help_desk.message_set.order_by('-created_at').first()
        if not last_message:
            return {}
        return MessageSerializer(instance=last_message).data


class MessageSerializer(serializers.ModelSerializer):
    help_desk = serializers.UUIDField(source="help_desk.uuid")

    class Meta:
        model = Message
        fields = ("created_at", "updated_at", "uuid", "message", "file", "type", "status", "help_desk",)
