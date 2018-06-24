from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import get_all_books, get_book_used, UserBook, get_one_unknown_word, UserWordsPlan, get_words_list
from words import models
from django.contrib.auth.models import User
from django.utils import timezone


def get_recite_next_word(request, user_name):
    request.session['is_recite_next'] = True
    return redirect('words:recite', user_name)


def recite(request, user_name):
    message = {'user_name': user_name}
    user = User.objects.get(username=user_name)
    book = UserBook.objects.filter(user=user, is_use=True).get().book
    plan = UserWordsPlan.objects.get(user=user)
    if request.method == 'GET':
        if 'words_recite_list' in request.session:
            if request.session['seq_now'] == plan.recite_words_day:
                return redirect('words:finish_recite', user_name)
            elif 'is_recite_next' in request.session and request.session['is_recite_next']:
                request.session['seq_now'] = request.session['seq_now'] + 1
                request.session['is_recite_next'] = False
        else:
            request.session['words_recite_list'] = get_words_list(user_name, book, plan.recite_words_day)
            request.session['seq_now'] = 1
        now_word = request.session['words_recite_list'][request.session['seq_now'] - 1]
        message['now_word'] = now_word
        message['can_show_content'] = False
        return render(request, 'words/recite.html', message)

    elif request.method == 'POST':
        now_word = request.session['words_recite_list'][request.session['seq_now'] - 1]
        message['now_word'] = now_word
        message['can_show_content'] = True
        if request.POST['if_remember'] == 'I know it':
            pass  # save to the database  TODO
        elif request.POST['if_remember'] == "I don't know it":
            pass  # TODO
        else:
            return HttpResponse('invalid post')
        return render(request, 'words/recite.html', message)


def manage(request, user_name):
    books = get_all_books()
    user = User.objects.get(username=user_name)
    plan = UserWordsPlan.objects.get(user=user)
    message = {'user_name': user_name,
               'books': books,
               'recite_word_day': plan.recite_words_day,
               'review_word_day': plan.review_words_day}

    if request.method == 'GET':
        book_used = get_book_used(user_name)
        if book_used != '':
            message['choose_book'] = book_used
        return render(request, 'words/manage.html', message)

    elif request.method == 'POST':
        choose_book = request.POST['choose_book']
        message['choose_book'] = choose_book
        query_used_set = UserBook.objects.filter(user=user, is_use=True)
        if query_used_set.exists():
            item = query_used_set.get()
            item.is_use = False
            item.save()
        query_set = UserBook.objects.filter(user=user, book_id=choose_book)
        if query_set.exists():
            item = query_set.get()
            item.is_use = True
            item.save()
        else:
            item = UserBook(user_id=user, book_id=choose_book, is_use=True)
            item.save()
        change_flag = False
        if plan.recite_words_day != request.POST['recite_word_day']:
            plan.recite_words_day = request.POST['recite_word_day']
            change_flag = True
        if plan.review_words_day != request.POST['review_word_day']:
            plan.review_words_day = request.POST['review_word_day']
            change_flag = True
        if change_flag:
            plan.save()
            message['recite_word_day'] = plan.recite_words_day
            message['review_word_day'] = plan.review_words_day
        return render(request, 'words/manage.html', message)


def finish_recite(request, user_name):
    message = {'user_name': user_name,
               }
    if request.method == 'GET':
        user = User.objects.get(username=user_name)
        date = timezone.now()
        if models.UserReciteRecord.objects.filter(user=user, date=date).exists():
            return render(request, 'words/finish_recite.html')
        else:
            item = models.UserReciteRecord(user=user, date=date)
            item.save()
        return render(request, 'words/finish_recite.html', message)
    elif request.method == 'POST':
        if request.POST['try_more'] == 'Sure':
            del request.session['words_recite_list']
            return redirect('words:recite', user_name)
        else:
            return redirect('users:index')

