from django.db import models

# Create your models here.


class Test(models.Model):
    name = models.CharField(unique=True, max_length=250)

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


# class Choices(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # name = models.CharField(max_length=1000)
    # isCorrect = models.BooleanField(default=False)

    # class Meta:
    #     unique_together = [
    #         # no duplicated choice per question
    #         ("question", "name")
    #     ]

    # def __str__(self):
    #     return self.name


class TestTaker(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(unique=True, max_length=250)

    def __str__(self):
        return self.name


class Answer(models.Model):
    answer_list = [('choice1', 'choice1'), ('choice2', 'choice2'),
                   ('choice3', 'choice3'), ('choice4', 'choice4')]
    testTaker = models.ForeignKey(TestTaker, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selectedChoice = models.CharField(max_length=8, choices=answer_list)
    isCorect = models.BooleanField(default=False)

    class Meta:
        unique_together = [
            # no duplicated choice per question
            ("question", "testTaker", 'test')
        ]

    def __str__(self):
        return self.testTaker.email, self.question.name, self.isCorect
