from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from django.utils import timezone

from .models import Question


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question
        """
        Fields whose name are passed in this list will be used to perform a
        Model.objects.get_or_create() instead of the usual Model.objects.create()
        """
        #django_get_or_create = ('question_text',)

    #question_text = "How do you do ?"
    # Use Fuzzy to generate random question text
    # you can use FuzzyAttribute, FuzzyText, FuzzyChoice, FuzzyInteger
    # FuzzyDecimal, FuzzyFloat, FuzzyDate, FuzzyDateTime, FuzzyNaiveDateTime
    # or Custom fuzzy fields to generate randome field data.
    # Reference: http://factoryboy.readthedocs.org/en/latest/fuzzy.html
    question_text = FuzzyText(length=20, prefix='Q:', suffix='?')
    pub_date = timezone.now()

