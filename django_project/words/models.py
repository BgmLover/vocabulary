from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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


class UserExamRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    question_num = models.IntegerField()
    right_num = models.IntegerField()
    note = models.CharField(max_length=200,default='')


class UserRecitedDefinedWords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey('words.UserDefinedWords', on_delete=models.CASCADE)


class UserWordsPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recite_words_day = models.IntegerField(default=20)
    review_words_day = models.IntegerField(default=10)
    examine_words = models.IntegerField(default=20)


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


def get_recited_words_list(user_name, book, size):
    user = User.objects.get(username=user_name)
    word_set = Words.objects.filter(book=book)
    total_size = word_set.count()
    recited_set = UserRecitedBookWords.objects.filter(user=user)
    count = 0
    words_list = []
    if size < total_size:
        while count <= size:
            random_index = random.randint(0, total_size-1)
            word = word_set[random_index]
            if word not in recited_set.filter(user=user):
                count = count + 1
                words_list.append(process_word(word, count))
    else:
        seq = 0
        for word in word_set:
            seq = seq + 1
            words_list.append(process_word(word, seq))
    return words_list


def get_review_words_list(user_name, size):
    user = User.objects.get(username=user_name)
    word_set = UserRecitedBookWords.objects.filter(user=user)
    total_size = word_set.count()
    count = 0
    words_list = []
    if size < total_size:
        while count <= size:
            random_index = random.randint(0, total_size-1)
            word = word_set[random_index]
            print(random_index)
            count = count + 1
            print(word.word_id)
            tmp_word = Words.objects.get(word=word.word_id)
            words_list.append(process_word(tmp_word, count))
    else:
        seq = 0
        for word in word_set:
            seq = seq + 1
            words_list.append(process_word(word, seq))
    return words_list


def recite_one_word(user_name, word):
    user = User.objects.get(username=user_name)
    user = User.objects.get(username=user)
    query_set = UserRecitedBookWords.objects.filter(user=user, word=word)
    if not query_set.exists():
        item = UserRecitedBookWords(user=user, word_id=word)
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


def get_exam_words(size, book_name):
    words_list = []
    words_set = Words.objects.filter(book_id=book_name)
    total_size = words_set.count()
    count = 0
    while count < size:
        random_index = random.randint(0, total_size - 1)
        random_word = process_word(words_set[random_index], count)
        if random_word not in words_list:
            count = count + 1
            words_list.append(random_word)
    return words_list


def save_an_exam_record(user_name, question_num, right_num, note=''):
    user = User.objects.get(username=user_name)
    item = UserExamRecord(user=user, question_num=question_num, right_num=right_num, note=note)
    item.date = timezone.now()
    item.save()

