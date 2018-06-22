from django.db import models
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
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    progress = models.FloatField(default=0)
    is_use = models.BooleanField(default=False)


class UserDefinedWords(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    word = models.CharField(max_length=30, unique=True)
    phonetic_symbol_e = models.CharField(max_length=100, null=True)
    phonetic_symbol_a = models.CharField(max_length=100, null=True)
    pronunciation_e = models.CharField(max_length=1000, null=True)
    pronunciation_a = models.CharField(max_length=1000, null=True)
    meanings = models.CharField(max_length=1000)
    example_sentence = models.CharField(max_length=1000, null=True)


class UserRecitedBookWords(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    word = models.ForeignKey('words.Words', on_delete=models.CASCADE)


# class UserUnRecitedBookWords(models.Model):
#     user = models.ForeignKey('users.User', on_delete=models.CASCADE)
#     word = models.ForeignKey('words.Words', on_delete=models.CASCADE)


class UserRecitedDefinedWords(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    word = models.ForeignKey('words.UserDefinedWords', on_delete=models.CASCADE)


def get_one_unknown_word(user_name, book_name):
    total_set = Words.objects.filter(book=book_name)
    recited_set = UserRecitedBookWords.objects.filter(user=user_name)
    for word in total_set:
        item = recited_set.filter(user=user_name, word=word.word)
        if not item.exists():
            return word


def get_one_known_word(user_name, book_name):
    recited_set = UserRecitedBookWords.objects.filter(user=user_name)
    size = recited_set.count()
    index = random.randrange(size)
    word = recited_set[index]
    return word


def recite_one_word(user_name, word):
    query_set = UserRecitedBookWords.objects.filter(user=user_name, word=word)
    if not query_set.exists():
        item = UserRecitedBookWords(user=user_name, word=word)
        item.save()


def forget_one_word(user_name, word):
    query_set = UserRecitedBookWords.objects.filter(user=user_name, word=word)
    if query_set.exists():
        query_set.delete()
