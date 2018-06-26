from django.shortcuts import render, redirect,reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import check_type
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import db
from words.models import UserBook, Books, UserWordsPlan


def index(request):
    if 'logged_in' in request.session and 'user_name' in request.session:
        return redirect('users:index_login', request.session['user_name'])
    return render(request, 'users/index.html')


@login_required
def index_login(request, user_name):
    print(request.user)
    message = {'logged_in': True, 'user_name': user_name}
    return render(request, 'users/index.html', message)


def sign_up(request):
    message = {'logged_in': True}
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
                user = User(username=username, email=email_address)
                user.set_password(password)
                user.save()
                books = Books.objects.all()
                plan = UserWordsPlan(user=user)
                plan.save()
                for book in books:
                    item = UserBook(user=user, book=book)
                    item.save()
                # create new user-book table
                return redirect('users:index')
            # the user information is duplicated
            except db.IntegrityError as e:
                print('shit')
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
        user_name = request.POST['User_identifier']
        message = {'logged_in': False, }
        usr = authenticate(request, username= user_name, password=password)
        if usr is not None:
            login(request, usr)
            message['logged_in'] = True
            message['user_name'] = user_name
            request.session['user_name'] = user_name
            request.session['logged_in'] = True
            return redirect('users:index_login', user_name)
        else:
            message['error'] = True
            return render(request, 'users/sign_in.html', message)


@login_required
def sign_out(request):
    logout(request)
    return redirect('users:index')







