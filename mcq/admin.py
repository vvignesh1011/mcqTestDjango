from django.contrib import admin
from . import models

# Register your models here.


# for Test
@admin.register(models.Test)
class TestAdmin(admin.ModelAdmin):
    list_display=('name','duration','noOfQuestions','marksPerQuestions')
    search_fields=('name',)
    sortable_by=('name',)



# for Questions
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=('name','test')
    search_fields=('name','test__name')
    sortable_by=('test',)
    list_filter=('test',)


# for Answers
@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display=('testTakerName','testName','question','isCorect')
    list_filter=('answerSheet__testTaker__name','answerSheet__test')
    search_fields=('answerSheet__testTaker__name',)
    sortable_by=('answerSheet__test',)


# for TestTaker
@admin.register(models.TestTaker)
class TestTakerAdmin(admin.ModelAdmin):
    list_display=('name','email')
    search_fields=('name','email')
    sortable_by=('name')
    

# for answerSheet
@admin.register(models.Answersheet)
class AnswersheetAdmin(admin.ModelAdmin):
    list_display = ('testTaker','test','isEnded','marks')
    list_filter=('test','testTaker')
    search_fields=('testTaker__name','test__name')
    sortable_by=('testTaker__name',)
# admin.site.register(models.Choices)
