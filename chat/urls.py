from django.urls import path

from chat.views import room

app_name = 'chat'

urlpatterns = [
    path('room/<int:course_id>/', room, name='room')
]
