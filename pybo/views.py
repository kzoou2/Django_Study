from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question,Answer
from django.http import HttpResponseNotAllowed
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

from django.http import HttpResp

def index(request):
    page = request.GET.get('page', '1')                      #페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)        #페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

# 질문 목록이 출력되도록
# def index(request):
#     question_list = Question.objects.order_by('-create_date')
#     context = {'question_list': question_list}
#     return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
gi

def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()
    # return redirect('pybo:detail', question_id=question.id)

    ##210폼
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():                         #폼이 유효하다면
            question = form.save(commit=False)      #임시저장하여 qeustion 객체를 리턴받음
            question.create_date = timezone.now()   #실제 저장을 위해 작성일시 설정
            question.save()                         #데이터를 실제로 저장
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form }
    return render(request, 'pybo/question_form.html',context)
