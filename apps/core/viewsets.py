from rest_framework import generics, views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.core.models import HelpDesk, Message
from apps.core.serializers import MessageSerializer, HelpDeskSerializer
from apps.core.tasks import handle_message


class HelpDesksList(generics.ListAPIView):
    serializer_class = HelpDeskSerializer
    queryset = HelpDesk.objects.order_by('-created_at')


class HelpDesksHistory(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        help_desk = get_object_or_404(HelpDesk, uuid=self.kwargs['uuid'])
        return Message.objects.filter(help_desk=help_desk).order_by('-created_at')


class SendMessageView(views.APIView):
    def post(self, request, *args, **kwargs):
        help_desk = get_object_or_404(HelpDesk, uuid=self.request.data['help_desk'])
        message = Message.objects.create(
            help_desk=help_desk,
            message=self.request.data.get('message'),
            file=self.request.FILES.get('file'),
            type=Message.TYPE_SENT
        )
        handle_message.delay(str(message.uuid))
        return Response({'message': 'Mensagem criada'})
