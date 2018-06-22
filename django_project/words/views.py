from django.shortcuts import render
from django.http import HttpResponse


def recite(request, user_name):
    message = {'user_name': user_name}
    return render(request, 'words/recite.html', message)

