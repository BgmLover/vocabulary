from django.shortcuts import render
from django.http import HttpResponse
from .models import get_all_books, get_book_used, UserBook


def recite(request, user_name):
    message = {'user_name': user_name}
    return render(request, 'words/recite.html', message)


def manage(request, user_name):
    books = get_all_books()
    message = {'user_name': user_name, 'books': books, 'book_size_range': range(books.__len__())}
    if request.method == 'GET':
        book_used = get_book_used(user_name)
        if book_used != '':
            message['choose_book'] = book_used
        return render(request, 'words/manage.html', message)
    elif request.method == 'POST':
        choose_book = request.POST['choose_book']
        print(choose_book)
        message['choose_book'] = choose_book
        query_used_set = UserBook.objects.filter(user=user_name, is_use=True)
        if query_used_set.exists():
            item = query_used_set.get()
            item.is_use = False
            item.save()
        query_set = UserBook.objects.filter(user=user_name, book_id=choose_book)
        if query_set.exists():
            item = query_set.get()
            item.is_use = True
            item.save()
        else:
            item = UserBook(user_id=user_name, book_id=choose_book, is_use=True)
            item.save()
        return render(request, 'words/manage.html', message)
