from django.db import models
import datetime
import random
import pytz

# Create your models here.


class Test(models.Model):
    name = models.CharField(unique=True, max_length=250)
    duration = models.IntegerField(
        default=0)
    noOfQuestions = models.IntegerField(blank=True, null=True)
    marksPerQuestions = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    name = models.TextField()
    choice1 = models.CharField(max_length=300, blank=True, null=True)
    choice2 = models.CharField(max_length=300, blank=True, null=True)
    choice3 = models.CharField(max_length=300, blank=True, null=True)
    choice4 = models.CharField(max_length=300, blank=True, null=True)
    answer_list = [('choice1', 'choice1'), ('choice2', 'choice2'),
                   ('choice3', 'choice3'), ('choice4', 'choice4')]
    correctAnswer = models.CharField(max_length=300, choices=answer_list)

    def __str__(self):
        return self.name


class TestTaker(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(unique=True, max_length=250)

    def __str__(self):
        return self.name


# answer sheet
class Answersheet(models.Model):
    testTaker = models.ForeignKey(TestTaker, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
    startedAt = models.DateTimeField(blank=True, null=True)
    endAt = models.DateTimeField(blank=True, null=True)
    marksPerQuestion = models.IntegerField(default=1)
    totalQuestions = models.IntegerField(default=0)
    submited = models.BooleanField(default=False)


    @property
    def isEnded(self):
        if (self.submited):
            return True
        if (self.duration):
            seconds = datetime.datetime.now(
                tz=pytz.timezone('Asia/Kolkata'))-self.startedAt
            duration = seconds.total_seconds()/60
            print(duration, 'duration')
            if (duration > self.duration):
                return True
        return False

    @property
    def marks(self):
        return self.getMarks()


    def __str__(self):
        return self.testTaker.name + " " + self.test.name + " {}".format(self.getMarks()) + 'marks'

# start test
    def startTest(self):
        totalQuestions = Answer.objects.filter(
            answerSheet=self.id).all().count()
        if (totalQuestions != 0):
            return

        try:
            test = Test.objects.get(id=self.test.id)
            self.marksPerQuestion = test.marksPerQuestions
            # self.duration = self.test.duration
            totalQuestions = Question.objects.filter(
                test=self.test.id).all().count()
            maxQuestions = test.noOfQuestions or totalQuestions
            self.totalQuestions = min(maxQuestions, totalQuestions)
            sequence = random.sample(
                range(0, totalQuestions), self.totalQuestions)
            questions = Question.objects.filter(test=self.test.id)

            print('totalqus', totalQuestions, maxQuestions)
            answers = []
            for x in sequence:
                answers.append(
                    Answer(answerSheet=self, question=questions[x]))

            self.startedAt = datetime.datetime.now(
                tz=pytz.timezone('Asia/Kolkata'))
            self.save()
            return answers

        except:
            raise

    def endTest(self):
        self.ended = True
        self.save()

    def getMarks(self):
        correctAns = Answer.objects.filter(
            answerSheet=self.id, isCorect=True).count()
        return correctAns*self.marksPerQuestion


class Answer(models.Model):
    answerSheet = models.ForeignKey(Answersheet, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selectedChoice = models.CharField(max_length=8, blank=True, null=True)
    isCorect = models.BooleanField(default=False)
    statusList = [('notAnswered', 'notAnswered'),
                  ('answered', 'answered'), ('inReview', 'inReview')]
    status = models.CharField(
        max_length=15, choices=statusList, default='notAnswered')
    
    @property 
    def testTakerName(self):
        return self.answerSheet.testTaker.name
    
    @property
    def testName(self):
        return self.answerSheet.test
    

    def __str__(self):
        return self.question.name+', {corect}'.format(corect=self.isCorect)
