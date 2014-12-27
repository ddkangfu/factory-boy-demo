import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.html import escape

from .factories import QuestionFactory


def create_question(question_text="Question", hours=None, days=None):
    params = {}

    if hours:
        params["hours"] = hours

    if days:
        params["days"] = days

    time = timezone.now() + datetime.timedelta(**params)
    return QuestionFactory(question_text=question_text, pub_date=time)


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        future_question = create_question(days=30)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        old_question = create_question(days=-30)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        recent_question = create_question(hours=-1)
        self.assertEqual(recent_question.was_published_recently(), True)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, escape("No polls are available."))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        create_question(question_text='Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, escape("No polls are available."), status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        create_question(question_text='Past question.', days=-30)
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        create_question(question_text='Past question 1.', days=-30)
        create_question(question_text='Past question 2.', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, escape(past_question.question_text), status_code=200)


class QuestionResultTests(TestCase):
    def test_result_view_with_no_question(self):
        response = self.client.get(reverse('polls:results', args=(555,)))
        self.assertEqual(response.status_code, 404)

    def test_result_view_with_a_question(self):
        question = create_question(question_text="My question.", days=-5)
        choice1 = question.choice_set.create(choice_text="Choice one.", votes=2)
        choice2 = question.choice_set.create(choice_text="Choice two.", votes=1)
        response = self.client.get(reverse('polls:results', args=(question.id,)))
        self.assertContains(response, escape(question.question_text), status_code=200)
        self.assertContains(response, escape(choice1.choice_text))
        self.assertContains(response, escape(choice2.choice_text))


class QuestionVoteTests(TestCase):
    def test_vote_view_with_no_question(self):
        response = self.client.post(reverse('polls:vote', args=(555, )))
        self.assertEqual(response.status_code, 404)

    def test_vote_view_with_inexist_choice(self):
        question = create_question(question_text="My question.", days=-5)
        response = self.client.post(reverse('polls:vote', args=(question.id,)), {'choice': 444})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, escape("You didn't select a choice."), status_code=200)

    def test_vote_view_with_exist_choice(self):
        question = create_question(question_text="My question.", days=-5)
        choice1 = question.choice_set.create(choice_text="Choice one.", votes=2)
        choice2 = question.choice_set.create(choice_text="Choice two.", votes=1)
        response = self.client.post(reverse('polls:vote', args=(question.id,)), {'choice': choice1.id})
        self.assertRedirects(response, reverse('polls:results', args=(question.id,)))
        #check votes number
        added_choice1 = question.choice_set.get(pk=choice1.id)
        self.assertEqual(added_choice1.votes, 3)
