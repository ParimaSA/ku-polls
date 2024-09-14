"""Provide test for voting."""
from django.test import TestCase
from polls.models import Question
from django.urls import reverse
from django.contrib.auth.models import User


def create_question(question_text):
    """Create a question with the given 'question_text'."""
    return Question.objects.create(question_text=question_text)


def create_choice(question, choice_num):
    """
    Create choice_num choices in question.

    choice_text = 1, 2, 3, ... , choice_num
    """
    for choice_text in range(1, choice_num+1):
        question.choice_set.create(choice_text=choice_text)


class VotingTest(TestCase):
    """Test voting systems, user can vote only after logged in and can vote only once."""

    def setUp(self):
        """Create a user for testing purposes."""
        self.user = User.objects.create_user(username='test', password='1234')

    def test_vote_with_authenticated_user(self):
        """Test that an authenticated user can vote and the vote is recorded correctly."""
        self.client.login(username='test', password='1234')
        question = create_question('test_question')
        create_choice(question, 2)
        choice = question.choice_set.all()
        response = self.client.post(reverse('polls:vote', args=[question.id]), {'choice': 1})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(choice[0].vote_set.count(), 1)
        self.assertEqual(choice[1].vote_set.count(), 0)

    def test_vote_without_authentication(self):
        """Test that an unauthenticated user cannot vote and is redirected to the login page."""
        question = create_question('test_question')
        create_choice(question, 2)
        response = self.client.post(reverse('polls:vote', args=[question.id]), {'choice': 1})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f"{reverse('login')}?next={reverse('polls:vote', args=[question.id])}")

    def test_multiple_votes(self):
        """Test that a user can only vote once per question (if applicable)."""
        question = create_question('test_question')
        create_choice(question, 2)
        choice = question.choice_set.all()
        self.client.login(username='test', password='1234')
        self.client.post(reverse('polls:vote', args=[question.id]), {'choice': 1})
        response = self.client.post(reverse('polls:vote', args=[question.id]), {'choice': 2})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(choice[0].vote_set.count(), 0)
        self.assertEqual(choice[1].vote_set.count(), 1)
