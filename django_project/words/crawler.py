import requests
import lxml.html
import json
from django.db import IntegrityError
from .models import Words
# the words book are from https://www.shanbay.com
toelf_basis = {'url': 'https://www.shanbay.com/wordlist/134137/298',
               'name': 'TOELF_Basis',
               'step': 3,
               'parts': 8,
               'start': 786}

toelf_middle = {'url': 'https://www.shanbay.com/wordlist/134146/298',
                'name': 'TOELF_Middle',
                'step': 3,
                'parts': 6,
                'start': 834}

toelf_advanced = {'url': 'https://www.shanbay.com/wordlist/134149/298',
                  'name': 'TOELF_Advanced',
                  'step': 3,
                  'parts': 6,
                  'start': 855}


def download_indexwords(book):
    directory = 'words_book/'
    urls = []

    t_meanings = []
    t_words = []

    for part in range(book['parts']):
        part_url = book['url'] + str(book['start'] + part * book['step']) + '/'
        for page_index in range(1, 11):
            url_list = part_url + '?page={}'.format(page_index)
            urls.append(url_list)
    for each in urls:
        print(each)
        html = requests.get(each).content
        selector = lxml.html.fromstring(html)
        meanings = selector.xpath('//tbody/tr/td[@class="span10"]/text()')
        words = selector.xpath('//tbody/tr/td[@class="span2"]/strong/text()')
        t_meanings = t_meanings+meanings
        t_words = t_words + words

    number_of_words = t_words.__len__()
    word_dict = {'book_name': book['name'], 'size': number_of_words, 'words': t_words, 'meanings': t_meanings}
    with open(directory + book['name'] + '.json', 'w+') as file:
        json.dump(word_dict, file)


def save_words(book_name):
    directory = 'words/words_book/'
    with open(directory + book_name + '.json', 'r') as file:
        words_dict = json.load(fp=file)

    base_url = 'https://www.youdao.com/w/'
    for word in words_dict['words']:
        url = base_url + word
        html = requests.get(url).content
        selector = lxml.html.fromstring(html)
        print(word)
        phonetic_symbol_e = selector.xpath('//h2[@class="wordbook-js"]/div[@class="baav"]/span[1]/span/text()')
        if len(phonetic_symbol_e) != 0:
            phonetic_symbol_e = phonetic_symbol_e[0]
            pronunciation_e = 'https://dict.youdao.com/dictvoice?audio=' + word + '&type=1'
        else:
            phonetic_symbol_e = ''
            pronunciation_e = ''
        phonetic_symbol_a = selector.xpath('//h2[@class="wordbook-js"]/div[@class="baav"]/span[last()]/span/text()')
        if len(phonetic_symbol_a) != 0:
            phonetic_symbol_a = phonetic_symbol_a[0]
            pronunciation_a = 'https://dict.youdao.com/dictvoice?audio=' + word + '&type=2'
        else:
            phonetic_symbol_a = ''
            pronunciation_a = ''

        meaning_list = selector.xpath('//div[@id="phrsListTab"]/div[@class="trans-container"]/ul/li/text()')
        meanings = ''
        for meaning in meaning_list:
            meanings = meanings + meaning + '<br>'
        meanings = meanings[:-4]
        english_spans = selector.xpath('//div[@id="examplesToggle"]/div[@id="bilingual"]/ul/li[1]/p[1]/span')
        english_sentence = ''
        chinese_sentence = ''
        chinese_spans = selector.xpath('//div[@id="examplesToggle"]/div[@id="bilingual"]/ul/li[1]/p[2]/span/text()')
        for span in chinese_spans:
            chinese_sentence = chinese_sentence + span
        for span in english_spans:
            content = span.xpath('text()')
            if len(content) != 0:
                english_sentence = english_sentence + content[0]
            else:
                text = span.xpath('b/text()')[0]
                english_sentence = english_sentence + text
        sentence = english_sentence + '<br>' + chinese_sentence

        try:
            new_word = Words(
                word=word,
                pronunciation_e=pronunciation_e,
                pronunciation_a=pronunciation_a,
                phonetic_symbol_e=phonetic_symbol_e,
                phonetic_symbol_a=phonetic_symbol_a,
                example_sentence=sentence,
                book=book_name,
                meanings=meanings
            )

            new_word.save()
        except IntegrityError:
            raise IntegrityError


# save_words('TOELF_Basis')
