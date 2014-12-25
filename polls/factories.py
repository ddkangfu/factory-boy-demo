import factory

from .models import Question, Choice


class QuestionFactory(factory.Factory):
    class Meta:
        model = Question

    question_text = "How do you do ?"
    pub_date = timezone.now()


"""
class ChoiceFactory(factory.Factory):
    class Meta:
        model = Choice
"""
