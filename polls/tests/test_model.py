"""Provide test for models in polls application."""
import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question


def create_question(question_text, days):
    """Create a question with the given 'question_text' and published 'days' offset to now.

    negative for questions published in the past,
    positive for questions that have not published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    """Test Question model has all method working properly."""

    def test_was_published_recently_with_future_question(self):
        """Test was_published_recently method for questions whose pub_date is in the future."""
        future = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=future)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        """Test was_published_recently method for questions whose pub_date is older than 1 day."""
        past = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=past)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        """Test was_published_recently method for questions whose pub_date is within last day."""
        in_one_day = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=in_one_day)
        self.assertTrue(recent_question.was_published_recently())

    def test_is_published_with_future_question(self):
        """Test is_published method for questions whose pub_date is in the future."""
        future = timezone.now() + datetime.timedelta(minutes=3)
        future_question = Question(pub_date=future)
        self.assertFalse(future_question.is_published())

    def test_is_published_with_recent_question(self):
        """Test is_published method returns for questions whose pub_date is current date-time."""
        recent = timezone.now()
        recent_question = Question(pub_date=recent)
        self.assertTrue(recent_question.is_published())

    def test_is_published_with_old_question(self):
        """Test is_published method returns for questions whose pub_date is older than current."""
        past = timezone.now() - datetime.timedelta(days=2)
        old_question = Question(pub_date=past)
        self.assertTrue(old_question.is_published())

    def test_can_vote_with_unpublished_question(self):
        """Test can_vote method for questions whose pub_date is in the future."""
        future = timezone.now() + datetime.timedelta(days=1)
        unpublished_question = Question(pub_date=future)
        self.assertFalse(unpublished_question.can_vote())

    def test_can_vote_with_closed_question(self):
        """Test can_vote method for questions whose end_date is in the past."""
        past = timezone.now() - datetime.timedelta(seconds=1)
        closed_question = Question(end_date=past)
        self.assertFalse(closed_question.can_vote())

    def test_can_vote_with_opened_question(self):
        """Test can_vote method for questions whose current date between pub and end_date."""
        future = timezone.now() + datetime.timedelta(days=1)
        opened_question = Question(end_date=future)
        self.assertTrue(opened_question.can_vote())

    def test_can_vote_with_opened_question_with_null_end_date(self):
        """Test can_vote method for questions whose pub_date is in the past and end_date is None."""
        past = timezone.now() - datetime.timedelta(days=1234)
        opened_question = Question(pub_date=past, end_date=None)
        self.assertTrue(opened_question.can_vote())
