from django.shortcuts import render, redirect

# Create your views here.

from .templates import *
from . import models
import random
import math


def mapwithAns(answers, answerSheet):
    # testTaker = models.TestTaker.objects.values().get(email=testTaker)

    def getAnswer(answer):
        # print(answer['question_id'], 'answer')
        # try:
        question = models.Question.objects.values().get(
            id=answer['question_id'])
        question['default'] = answer['selectedChoice']
        print(question, 'answer')
        return question
        # except:
        #     print('no answer')
        #     return answers
        # else:
        #     question['default'] = answer['selectedChoice']
        # finally:
        #     return question

    questions = map(getAnswer, answers)
    return questions


def saveAns():
    pass


def index(request):
    testTaker = request.session.get('testTaker', False)
    page = request.session.get('page', 1)
    sortby = request.session.get('sortby')
    startFrom = request.session.get('startFrom')
    testId = request.session.get('testId')

    print(testTaker, page, sortby, startFrom, testId)

    if not (testTaker):
        return redirect('/login')

    test = models.Test.objects.get(id=testId)
    testTaker = models.TestTaker.objects.get(email=testTaker)
    answerSheet = models.Answersheet.objects.filter(
        test=test, testTaker=testTaker).first()

    if (not answerSheet):
        answerSheet = models.Answersheet(test=test, testTaker=testTaker)
    answers = answerSheet.startTest()
    if (answers):
        for ans in answers:
            ans.save()

    total = models.Answer.objects.filter(answerSheet=answerSheet.id).count()
    answers = models.Answer.objects.filter(answerSheet=answerSheet.id).values().all()[
        (page*10)-10:(page*10)]
    totalPage = math.ceil(total/10)
    end = page == totalPage
    start = (page == 1)
    # print(page, start, 'page', total, answers)

    questions = mapwithAns(answers, answerSheet)

    return render(request, "index.html", {'questions': questions, "page": page, 'totalPage': totalPage, 'end': end, 'start': start})


def login(request):
    if request.method == 'POST':
        form = request.POST
        print(form['email'])
        try:
            testTaker = models.TestTaker.objects.filter(
                email__contains=form['email'])[0]
            print('testTaker', testTaker)
        except:
            testTaker = models.TestTaker(
                name=form['name'], email=form['email'])
            testTaker.save()

        sortby = {1: 'choice1', 2: 'choice2', 3: 'choice3',
                  4: 'choice4', 5: 'name', 6: 'answer_list'}
        request.session.__setitem__('testTaker', testTaker.email)
        request.session.__setitem__('testId', form['test'])
        request.session.__setitem__('sortby', sortby[random.randint(1, 6)])

        return redirect('/')

    testTaker = request.session.get('testTaker')
    if testTaker:
        return redirect('/')
    test = models.Test.objects.all().values()
    print('test', test)
    return render(request, "login.html", {"test": test})


def submit(request):
    testTaker = models.TestTaker.objects.get(
        email=request.session.get('testTaker'))
    page = request.session.get('page', 1)

    test = models.Test.objects.get(id=request.session.get('testId'))
    resultPage = False

    if (request.method == 'POST'):
        form = request.POST
        print(form)
        answerSheet = models.Answersheet.objects.get(
            test=test.id, testTaker=testTaker.id)
        for x in form:
            if (x != 'csrfmiddlewaretoken' and x != 'submit' and x != 'prev' and x != 'next'):
                question = models.Question.objects.get(id=x)

                isCorrect = question.correctAnswer == form[x]
                try:
                    answer = models.Answer.objects.get(
                        question=question.id, answerSheet=answerSheet.id)
                except:
                    pass
                    # answer = models.Answer(
                    #     testTaker=testTaker, test=test, question=question, selectedChoice=form[x], isCorect=isCorrect)
                else:
                    answer.selectedChoice = form[x]
                    answer.isCorect = isCorrect

                answer.save()
                print('answer', answer)

            # for pagination
            if (x == 'next'):
                request.session.__setitem__('page', page+1)
            if (x == 'prev'):
                request.session.__setitem__('page', page-1)
            if (x == 'submit'):
                resultPage = True
        if (resultPage):
            return redirect('result')
        return redirect('/')


def getResult(request):
    testTaker = request.session.get('testTaker', False)
    testTaker = models.TestTaker.objects.filter(
        email__contains=testTaker)[0]
    testId = request.session.get('testId')

    answerSheet = models.Answersheet.objects.get(
        test=testId, testTaker=testTaker.id)
    total = answerSheet.getMarks()

    # total = models.Answer.objects.filter(
    #     testTaker=testTaker['id'], test=testId, isCorect=True).count()

    return render(request, 'result.html', {'total': total})


def logout(reqest):
    reqest.session.flush()
    return redirect('/')
