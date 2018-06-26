from django.core.management.base import BaseCommand, CommandError
from words.models import get_one_unknown_word, get_one_known_word


class Command(BaseCommand):
    help = 'Please add the book_name'

    def add_arguments(self, parser):
        parser.add_argument('type', type=str)

    def handle(self, *args, **options):
        get_type = options['type']
        if get_type == 'unknown':
            get_one_unknown_word('zq', 'TOEFL_Basis')
        else:
            get_one_known_word('zq', 'TOEFL_Basis')

