from django.core.management.base import BaseCommand, CommandError
from words.crawler import save_words

class Command(BaseCommand):
    help = 'Please add the book_name'

    def add_arguments(self, parser):
        parser.add_argument('book_name', type=str)

    def handle(self, *args, **options):
        book_name = options['book_name']
        save_words(book_name)
