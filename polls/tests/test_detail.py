"""Provide test for detail page."""
import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from django.urls import reverse


def create_question(question_text, days):
    """Create a question with the given 'question_text' and published 'days' offset to now.

    negative for questions published in the past,
    positive for questions that have not published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionDetailViewTests(TestCase):
    """Test Index view response correctly."""

    def test_future_question(self):
        """
        Test detail view of a question with a pub_date in the future.

        Page should return a 302, page redirect to index page with error message.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertContains(self.client.get(response.url), 'Question not found')

    def test_past_question(self):
        """
        Test detail view of a question with a pub_date in the past.

        Page should display the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_user_has_not_voted(self):
        """
        Test detail view of a question with a user has not voted for this question.

        Page should not display the delete vote button.
        """
        question = create_question(question_text='Question', days=0)
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertNotContains(response, "Delete Vote")
