from django.shortcuts import render
from django.http import HttpResponseForbidden

from users.models import Profile


def room(request, course_id):

    return render(request, template_name='chat/room.html',
                  context={'course_id': course_id})




