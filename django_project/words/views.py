from django.shortcuts import render, redirect
from .models import get_all_books, get_book_used, UserBook, UserRecitedBookWords, \
    UserWordsPlan, get_recited_words_list, get_review_words_list, recite_one_word, \
    get_exam_words, UserReviewRecord, UserReciteRecord, save_an_exam_record,get_books_progress,get_defined_words,UserDefinedWords
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def get_recite_next_word(request, user_name):
    request.session['is_recite_next'] = True
    return redirect('words:recite', user_name)


def get_review_next_word(request, user_name):
    request.session['is_review_next'] = True
    return redirect('words:review', user_name)


@login_required
def recite(request, user_name):
    message = {'logged_in': True, 'user_name': user_name}
    user = User.objects.get(username=user_name)
    book = UserBook.objects.filter(user=user, is_use=True).get().book
    plan = UserWordsPlan.objects.get(user=user)
    if request.method == 'GET':
        if 'words_recite_list' in request.session:
            if request.session['seq_recite_now'] == plan.recite_words_day:
                return redirect('words:finish_recite', user_name)
            elif 'is_recite_next' in request.session and request.session['is_recite_next']:
                request.session['seq_recite_now'] = request.session['seq_recite_now'] + 1
                request.session['is_recite_next'] = False
        else:
            request.session['words_recite_list'] = get_recited_words_list(user_name, book, plan.recite_words_day)
            request.session['seq_recite_now'] = 1
        now_word = request.session['words_recite_list'][request.session['seq_recite_now'] - 1]
        message['now_word'] = now_word
        message['can_show_content'] = False
        return render(request, 'words/recite.html', message)

    elif request.method == 'POST':
        now_word = request.session['words_recite_list'][request.session['seq_recite_now'] - 1]
        message['now_word'] = now_word
        message['can_show_content'] = True
        if request.POST['if_remember'] == 'I know it':
            pass
        elif request.POST['if_remember'] == "I don't know it":
            pass
        recite_one_word(user_name, now_word['word'])
        return render(request, 'words/recite.html', message)


@login_required
def review(request, user_name):
    message = {'logged_in': True, 'user_name': user_name}
    user = User.objects.get(username=user_name)
    plan = UserWordsPlan.objects.get(user=user)

    if request.method == 'GET':
        if 'words_review_list' in request.session:  # 已经加载复习单词列表
            if request.session['seq_review_now'] == plan.recite_words_day:  # 复习完毕
                return redirect('words:finish_review', user_name)
            elif request.session['seq_review_now'] == len(request.session['words_review_list']):    # 复习完毕（可复习单词量少于计划）
                return redirect('words:finish_review', user_name)
            elif 'is_review_next' in request.session and request.session['is_review_next']:     # 复习过程中下一个单词请求
                request.session['seq_review_now'] = request.session['seq_review_now'] + 1
                request.session['is_review_next'] = False
        else:      # 还未加载复习单词列表
            request.session['words_review_list'] = get_review_words_list(user_name, plan.recite_words_day)
            request.session['seq_review_now'] = 1

        now_word = request.session['words_review_list'][request.session['seq_review_now'] - 1]
        message['now_word'] = now_word
        message['can_show_content'] = False
        return render(request, 'words/review.html', message)
    elif request.method == 'POST':
        now_word = request.session['words_review_list'][request.session['seq_review_now'] - 1]
        message['now_word'] = now_word
        message['can_show_content'] = True
        if request.POST['if_remember'] == 'I know it':
            pass
        elif request.POST['if_remember'] == "I don't know it":
            query_set = UserRecitedBookWords.objects.filter(user=user, word_id=now_word)
            if query_set.exists():
                query_set.delete()
        return render(request, 'words/review.html', message)


@login_required
def define_words(request, user_name):
    message = {'logged_in': True,
               'user_name': user_name,
               'defined_words': get_defined_words(user_name)
               }
    return render(request, 'words/define_words.html', message)


@login_required
def manage(request, user_name):
    book_info = get_books_progress(user_name)
    user = User.objects.get(username=user_name)
    plan = UserWordsPlan.objects.get(user=user)
    message = {'logged_in': True,
               'user_name': user_name,
               'book_info': book_info,
               'recite_word_day': plan.recite_words_day,
               'review_word_day': plan.review_words_day,
               'examine_word': plan.examine_words}

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
            #
            # if item.book_id != choose_book:
            #     del request.session['words_recite_list']
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
    message = {'logged_in': True,
               'user_name': user_name,
               }
    if request.method == 'GET':
        user = User.objects.get(username=user_name)
        date = timezone.now().date()
        if UserReciteRecord.objects.filter(user=user, date=date).exists():
            return render(request, 'words/finish_recite.html', message)
        else:
            item = UserReciteRecord(user=user, date=date)
            item.save()
        return render(request, 'words/finish_recite.html', message)
    elif request.method == 'POST':
        if request.POST['try_more'] == 'Sure':
            del request.session['words_recite_list']
            return redirect('words:recite', user_name)
        else:
            return redirect('users:index')


def finish_review(request, user_name):
    message = {'logged_in': True,
               'user_name': user_name}
    if request.method == 'GET':
        user = User.objects.get(username=user_name)
        date = timezone.now().date()
        if UserReviewRecord.objects.filter(user=user, date=date).exists():
            return render(request, 'words/finish_review.html', message)
        else:
            item = UserReviewRecord(user=user, date=date)
            item.save()
        return render(request, 'words/finish_review.html', message)
    elif request.method == 'POST':
        if request.POST['try_more'] == 'Sure':
            del request.session['words_review_list']
            return redirect('words:review', user_name)
        else:
            return redirect('users:index')


def finish_examine(request, user_name):
    message = {'logged_in': True,
               'user_name': user_name, "exam_info": request.session['exam_info']}
    if request.method == 'GET':
        return render(request, 'words/finish_examine.html', message)
    elif request.method == 'POST':
        if request.POST['try_more'] == 'Sure':
            del request.session['exam_words']
            del request.session['in_examining']
            del request.session['seq_now']
            return redirect('words:examine', user_name)
        elif request.POST['try_more'] == 'Review the exam':
            request.session['review'] = True
            request.session['in_examining'] = False
            return redirect('words:examine', user_name)
        else:
            request.session['review'] = False
            request.session['in_examining'] = False
            return redirect('users:index')


@login_required
def examine(request, user_name):
    message = {'logged_in': True,
               'user_name': user_name}
    user = User.objects.get(username=user_name)
    book = UserBook.objects.filter(user=user, is_use=True).get().book_id
    plan = UserWordsPlan.objects.get(user=user)

    if request.method == 'GET':
        if 'in_examining' not in request.session:
            request.session['exam_words'] = get_exam_words(plan.examine_words, book)
            request.session['seq_now'] = 0
            request.session['in_examining'] = True  # 正在考试
            message['exam_words'] = request.session['exam_words']
            message['in_examining'] = True
            message['seq_now'] = 0
            return render(request, 'words/examine.html', message)
        elif request.session['in_examining']:      # 还在考试（考虑到用户中途退出）
            print(request.session['in_examining'])
            message['exam_words'] = request.session['exam_words']
            message['in_examining'] = True
            message['seq_now'] = request.session['seq_now']
            return render(request, 'words/examine.html', message)
        else:                                       # 考完了
            if 'review' in request.session and request.session['review']:  # 考完后回顾
                message['exam_words'] = request.session['exam_words']
                message['in_examining'] = False
                message['seq_now'] = 0
                return render(request, 'words/examine.html', message)
            else:
                return redirect('words:finish_examine', user_name=user_name)

    elif request.method == 'POST':
        right_count = 0
        question_count = 0
        for word in request.session['exam_words']:
            question_count = question_count + 1
            if request.POST[word['word']+'_if_remember'] == 'true':
                right_count = right_count + 1
        save_an_exam_record(user_name=user_name, question_num=question_count, right_num=right_count)
        request.session['in_examine'] = False   # 宣布考完试
        request.session['exam_info'] = {'question_count': question_count, 'right_count': right_count}
        return redirect('words:finish_examine', user_name)
