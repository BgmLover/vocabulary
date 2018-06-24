from django.db import models
from django.contrib.auth.models import User
import random


class Words(models.Model):
    book = models.ForeignKey('words.Books', on_delete=models.CASCADE)
    word = models.CharField(max_length=30, primary_key=True)
    phonetic_symbol_e = models.CharField(max_length=100, null=True)
    phonetic_symbol_a = models.CharField(max_length=100, null=True)
    pronunciation_e = models.CharField(max_length=1000, null=True)
    pronunciation_a = models.CharField(max_length=1000, null=True)
    meanings = models.CharField(max_length=1000)
    example_sentence = models.CharField(max_length=1000, null=True)


class Books(models.Model):
    book_name = models.CharField(max_length=100, primary_key=True)


class UserBook(models.Model):
    book = models.ForeignKey('words.Books', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    progress = models.FloatField(default=0)
    is_use = models.BooleanField(default=False)


class UserDefinedWords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=30, unique=True)
    phonetic_symbol_e = models.CharField(max_length=100, null=True)
    phonetic_symbol_a = models.CharField(max_length=100, null=True)
    pronunciation_e = models.CharField(max_length=1000, null=True)
    pronunciation_a = models.CharField(max_length=1000, null=True)
    meanings = models.CharField(max_length=1000)
    example_sentence = models.CharField(max_length=1000, null=True)


class UserRecitedBookWords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey('words.Words', on_delete=models.CASCADE)


#  用戶背誦記錄，有記錄說明當天完成了記錄
class UserReciteRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()


class UserReviewRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()


class UserRecitedDefinedWords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey('words.UserDefinedWords', on_delete=models.CASCADE)


class UserWordsPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recite_words_day = models.IntegerField(default=20)
    review_words_day = models.IntegerField(default=10)


def get_one_unknown_word(user_name, book_name):
    total_set = Words.objects.filter(book=book_name)
    user = User.objects.get(username=user_name)
    recited_set = UserRecitedBookWords.objects.filter(user=user)
    for word in total_set:
        item = recited_set.filter(user=user, word=word.word)
        if not item.exists():
            return process_word(word, 0)


def process_word(word, seq):
    res_word = {'word': word.word,
                'book': word.book.book_name,
                'phonetic_symbol_e': word.phonetic_symbol_e,
                'phonetic_symbol_a': word.phonetic_symbol_e,
                'pronunciation_e': word.pronunciation_e,
                'pronunciation_a': word.pronunciation_a,
                'meanings': word.meanings.split('<br>'),
                'example_sentence': word.example_sentence.split('<br>'),
                'seq': seq}
    return res_word


def get_one_known_word(user_name, book_name):
    user = User.objects.get(username=user_name)
    recited_set = UserRecitedBookWords.objects.filter(user=user)
    size = recited_set.count()
    index = random.randrange(size)
    word = recited_set[index]
    return word


def get_words_list(user_name, book, size):
    user = User.objects.get(username=user_name)
    word_set = Words.objects.filter(book=book)
    total_size = word_set.count()
    recited_set = UserRecitedBookWords.objects.filter(user=user)
    count = 0
    words_list = []
    while count <= size:
        random_index = random.randint(0, total_size)
        word = word_set[random_index]
        if word not in recited_set.filter(user=user):
            count = count + 1
            words_list.append(process_word(word, count))
    return words_list


def recite_one_word(user_name, word):
    user = User.objects.get(username=user_name)
    user = User.objects.get(username=user)
    query_set = UserRecitedBookWords.objects.filter(user=user, word=word)
    if not query_set.exists():
        item = UserRecitedBookWords(user=user_name, word=word)
        item.save()


def forget_one_word(user_name, word):
    user = User.objects.get(username=user_name)
    query_set = UserRecitedBookWords.objects.filter(user=user, word=word)
    if query_set.exists():
        query_set.delete()


def get_all_books():
    books = Books.objects.all()
    books_list = []
    for book in books:
        books_list.append(book.book_name)
    return books_list


def get_book_used(user_name):
    user = User.objects.get(username=user_name)
    query_set = UserBook.objects.filter(user=user, is_use=True)
    if query_set.exists():
        return query_set.get().book.book_name
    else:
        return ''
