import time

from apps.core.models import Message
from chat.celery import app


@app.task
def handle_message(uuid):
    message = Message.objects.filter(uuid=uuid).first()
    while not message:
        message = Message.objects.filter(uuid=uuid).first()

    time.sleep(3)

    message.status = Message.STATUS_SENT
    message.save()

    time.sleep(1)

    Message.objects.create(
        help_desk=message.help_desk,
        message=f"Resposta - {message.message or ''}",
        file=message.file,
        type=Message.TYPE_RECEIVED,
        status=Message.STATUS_SENT
    )
    return
