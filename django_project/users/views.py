from django.shortcuts import render, redirect,reverse
from .models import User,check_type
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django import db


def index(request):
    return render(request, 'users/index.html')


def index_login(request, user_name):
    message = {'logged_in': True, 'user_name': user_name}
    return render(request, 'users/index.html', message)


def sign_up(request):
    if request.method == 'GET':
        return render(request, 'users/sign_up.html')
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        email_address = request.POST['Email']
        message = {'password': password, 'email_address': email_address, 'user_name': username}

        # to check if the user information is empty
        if username == '':
            message['empty'] = True
            message['error'] = "The username can't be empty"
            return render(request, 'users/sign_up.html', message)
        if password == '':
            message['empty'] = True
            message['error'] = "The password can't be empty"
            return render(request, 'users/sign_up.html', message)
        if email_address == '':
            message['empty'] = True
            message['error'] = "The email_address can't be empty"
            return render(request, 'users/sign_up.html', message)
        # to check if the user information's format is valid
        check_result = check_type(password, email_address)
        if not check_result['valid']:
            message['invalid_format'] = True
            message['error'] = check_result['content']
            return render(request, 'users/sign_up.html', message)
        if check_type(password, email_address):
            try:
                user = User(user_name=username, password=password,
                            email_address=email_address, register_date=timezone.now())
                user.save()
                return redirect('users:sign_in')
            # the user information is duplicated
            except db.IntegrityError as e:
                cause = e.__cause__
                message['info_duplicated'] = True
                if cause.__str__().find('email_address') != -1:
                    message['error'] = 'The email_address '+email_address+'has been used'
                    message['email_address'] = ''
                if cause.__str__().find('user_name') != -1:
                    message['error'] = 'The user_name   '+username+'  has been used'
                    message['user_name'] = ''
                return render(request, 'users/sign_up.html', message)
    return HttpResponse('fail')


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'users/sign_in.html')
    if request.method == 'POST':
        password = request.POST['Password']
        user_identifier = request.POST['User_identifier']
        message = {'logged_in': False, }

        # to check if the information is stored in the database
        if user_identifier.find('@') != -1:
            result = User.objects.filter(email_address=user_identifier).filter(password=password)
            if result.count() == 0:
                message['error'] = True
                return render(request, 'users/sign_in.html', message)
            else:
                message['logged_in'] = True
                message['user_name'] = result.get(email_address=user_identifier).user_name
                return redirect('users:index_login', user_name=message['user_name'])
        else:
            result = User.objects.filter(user_name=user_identifier).filter(password=password)
            if result.count() == 0:
                message['error'] = True
                message['user_name'] = user_identifier
                return render(request, 'users/sign_in.html', message)
            else:
                message['logged_in'] = True
                return redirect('/'+user_identifier+'/index')
                # print(reverse('users:index_login', args=(user_identifier,)))
                # return HttpResponseRedirect(reverse('users:index_login', args=(user_identifier,)))







