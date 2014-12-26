from factory.django import DjangoModelFactory

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

    question_text = "How do you do ?"
    pub_date = timezone.now()

