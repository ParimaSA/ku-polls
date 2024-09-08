import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from django.urls import reverse


def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published
    the given number of 'days' offset to now
    (negative for questions published in the past,
     positive for questions that have not published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionDetailViewTests(TestCase):
    """Test Index view response correctly"""

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302, page redirect to index page with error message.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        follow_response = self.client.get(response.url)
        self.assertContains(follow_response, 'Question not found')

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)