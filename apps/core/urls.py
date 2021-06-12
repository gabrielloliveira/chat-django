from django.urls import path
from . import viewsets

app_name = 'core'

urlpatterns = [
    path('help-desks/', viewsets.HelpDesksList.as_view(), name='help-desks'),
    path('help-desks/<uuid:uuid>/', viewsets.HelpDesksHistory.as_view(), name='help-desk-history'),
    path('send-message/', viewsets.SendMessageView.as_view(), name='send-message'),
]
