import datetime
from django.utils import timezone
from django.db import models


class Question(models.Model):
    """
    Question model contain two columns, question_text and pub_date.
    Question will be published after pub_date.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        """Return text of Question"""
        return self.question_text

    def was_published_recently(self):
        """
        Check whether the question was published within 1 day.
        If the question was published longer or has not published yet, return False.
        """
        return (timezone.now() - datetime.timedelta(days=1)) <= self.pub_date <= timezone.now()


class Choice(models.Model):
    """
    Choice model contain three columns, question, choice_text and votes.
    Choice links with question within Question. If that question was deleted, this choice will be deleted too.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return text of Choice"""
        return self.choice_text
