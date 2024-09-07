import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """
    Question model contain two columns, question_text and pub_date.
    Question will be published after pub_date.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    end_date = models.DateTimeField(null=True, default=None)

    def __str__(self):
        """Return text of Question"""
        return self.question_text

    def was_published_recently(self):
        """
        Check whether the question was published within 1 day.
        If the question was published longer or has not published yet, return False.
        """
        one_day_ago = (timezone.now() - datetime.timedelta(days=1))
        return one_day_ago <= self.pub_date <= timezone.now()

    def is_published(self):
        """
        Check whether the current date-time is on or after question’s publication date.
        If the question was not published yet, return False.
        """
        return self.pub_date <= timezone.now()

    def can_vote(self):
        """
        Check whether the question is between the pub_date and end_date.
        If the question was not published yet or
        the current date-time past the end_date, return False.
            (the end_date is null => the question is opened forever)
        """
        return self.pub_date <= timezone.now() and (self.end_date is None or
                                                    self.end_date >= timezone.now())


class Choice(models.Model):
    """
    Choice model contain three columns, question, choice_text and votes.
    Choice links with question within Question.
    If that question was deleted, this choice will be deleted too.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    @property
    def votes(self):
        """Return votes for this choice"""
        return self.vote_set.count()

    def __str__(self):
        """Return text of Choice"""
        return self.choice_text


class Vote(models.Model):
    """A vote by a user for a choice in a poll."""
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

