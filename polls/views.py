from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from polls.models import Choice, Question


class IndexView(generic.ListView):
    """Home page, contain list of questions that have been published within 1 day."""
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


def detail(request, question_id):
    """Detail page, contain choices for question."""
    try:
        question = Question.objects.get(pk=question_id)
        if not question.is_published():
            messages.error(request, "Question not found")
            return HttpResponseRedirect(reverse('polls:index'))
        if not question.can_vote():
            messages.error(request, "Section closed for voting")
            return HttpResponseRedirect(reverse('polls:index'))
        return render(request, 'polls/detail.html', context={'question': question})
    except (KeyError, Question.DoesNotExist):
        messages.error(request, "Question not found")
        return HttpResponseRedirect(reverse('polls:index'))


class ResultsView(generic.DetailView):
    """Result page, contain result vote from user for questionZz."""
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """
    Handle when the user click vote.
    If user does not select any choice, send back detail page with error message.
    Otherwise, add votes for that choice and send back results page.
    """
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "Section closed for voting")
        return HttpResponseRedirect(reverse('polls:index'))
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        messages.error(request, "You did not select a choice.")
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
