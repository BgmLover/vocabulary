from django.core.management.base import BaseCommand, CommandError
from words.crawler import save_words

from words.models import Books, Words


class Command(BaseCommand):
    help = 'Please add the book_name'

    def add_arguments(self, parser):
        parser.add_argument('book_name', type=str)

    def handle(self, *args, **options):
        book_name = options['book_name']
        book = Books(book_name=book_name)
        words_num = Words.objects.filter(book_id=book_name).count()
        book.total_words = words_num
        book.save()
        print(words_num)
