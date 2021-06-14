import uuid

from django.db import models


class DefaultBaseModel(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        abstract = True


class Client(DefaultBaseModel):
    name = models.CharField("Nome", max_length=200)
    phone = models.CharField("Telefone", max_length=200)

    def __str__(self):
        return self.name


class HelpDesk(DefaultBaseModel):
    client = models.ForeignKey(Client, verbose_name="Cliente", on_delete=models.CASCADE)
    organization = models.CharField("Organização", max_length=255, default="org1")

    def __str__(self):
        return str(self.uuid)


class Message(DefaultBaseModel):
    TYPE_RECEIVED = "received"
    TYPE_SENT = "sent"
    TYPE_CHOICES = (
        (TYPE_RECEIVED, "Recebida"),
        (TYPE_SENT, "Enviada"),
    )
    STATUS_SENT = 'sent'
    STATUS_SENDING = 'sending'
    STATUS_CHOICES = (
        (STATUS_SENDING, 'Enviando'),
        (STATUS_SENT, 'Enviado'),
    )
    help_desk = models.ForeignKey(HelpDesk, verbose_name="Atendimento", on_delete=models.CASCADE)
    message = models.TextField("Mensagem", blank=True, null=True)
    file = models.FileField("Arquivo", blank=True, null=True, upload_to="uploads/")
    type = models.CharField("Tipo da mensagem", choices=TYPE_CHOICES, default=TYPE_SENT, max_length=50)
    status = models.CharField("Status", choices=STATUS_CHOICES, default=STATUS_SENDING, max_length=50)

    def __str__(self):
        return f"{self.type} - {self.help_desk.uuid}"
