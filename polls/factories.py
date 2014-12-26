import factory

from django.utils import timezone

from .models import Question, Choice


class QuestionFactory(factory.Factory):
    class Meta:
        model = Question
        strategy = factory.CREATE_STRATEGY

    question_text = "How do you do ?"
    pub_date = timezone.now()


"""
class ChoiceFactory(factory.Factory):
    class Meta:
        model = Choice
"""
